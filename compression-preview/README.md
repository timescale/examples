# Chunk visualizer

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app)
and it basically connects to a [hasura](http://hasura.io) graphql api to visualize [hypertable chunks](https://tsdb.co/hasuracon-hypertables-docs) of a [TimescaleDB](https://timescale.com) instance. If you don't have an instance, you can get a free one [here](https://tsdb.co/hasuracon-signup).

[Hypertables](https://tsdb.co/hasuracon-hypertables-docs) are an abstract table representation that empowers timeseries storage for postgresql databases. The yellow circles represents the compressed data and the dark represents the uncompressed.

<img width="1250" alt="Screen Shot 2021-06-16 at 15 14 44" src="https://user-images.githubusercontent.com/15484/122271279-a0604c00-ceb5-11eb-8a3f-857645ec783d.png">


The idea here is collect this metadata from the "chunks" that are like subtables of the hypertables.

Here is a simple view with the chunks information aggregating data from different sources:

```sql
CREATE OR REPLACE VIEW chunks_with_compression AS
SELECT DISTINCT ch.chunk_name,
                ccs.chunk_schema,
                ch.hypertable_schema,
                ch.hypertable_name,
                ch.range_start,
                ch.range_end,
                COALESCE(ccs.before_compression_total_bytes, NULL, cds.total_bytes) AS before_compression_total_bytes,
                ccs.after_compression_total_bytes
FROM (
 SELECT hypertable_schema,
    hypertable_name,
    chunk_name,
    range_start,
    range_end
 FROM  timescaledb_information.chunks) AS ch
LEFT OUTER JOIN LATERAL chunk_compression_stats(ch.hypertable_name::regclass) ccs
ON              ch.chunk_name = ccs.chunk_name
LEFT OUTER JOIN LATERAL chunks_detailed_size(ch.hypertable_name::regclass) cds
ON              ccs.chunk_schema = cds.chunk_schema
AND             ch.chunk_name = cds.chunk_name;
```

With this query, you can get all details about chunk size and what limits they
cover in the data that is inside the database.

## A minimum hypertable example:


If you don't have a database do test, here is a minimal example to have some
data and test how it goes.

In this example, we're creating a table `conditions` that belongs to some
`device` and output some `temperature` to a given `time`.

```sql
CREATE TABLE conditions (
      time TIMESTAMPTZ NOT NULL,
      device INTEGER NOT NULL,
      temperature FLOAT NOT NULL,
      PRIMARY KEY(time, device)
);
SELECT * FROM create_hypertable('conditions', 'time', 'device', 3);

INSERT INTO conditions
SELECT time, (random()*30)::int, random()*80 - 40
FROM generate_series(TIMESTAMP '2020-01-01 00:00:00',
                 TIMESTAMP '2020-01-01 00:00:00' + INTERVAL '1 month',
             INTERVAL '1 min') AS time;
```

By default, we're inserting a month for testing purposes, but you can get deep
adding more data in the sequence.

You can try the following query to append 6 months of data right one week after the
previous data was added.

```sql
INSERT INTO conditions WITH latest AS ( SELECT time FROM conditions ORDER BY time DESC LIMIT 1 )
SELECT generate_series(latest.time + INTERVAL '1 week', latest.time + INTERVAL '6 month', INTERVAL '1 min') AS time,
(random()*30)::int as device, random()*80 - 40 AS temperature from latest;
```

The insert will append new data with one week interval to guarantee we don't
touch any previous chunk but creates new ones. It keeps inserting around 40k records
per month.


### Testing the compression

Now it comes the cool part, let's add a compression policy to automatically use
the `device` column as our main segment.

```sql
ALTER TABLE conditions SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device'
);
```

And then we can also set how many days after the record is inserted we want to
automatically compress:

```sql
SELECT add_compression_policy('conditions', INTERVAL '7 days');
```

So, it means that 7 days after the `time` of the insertion, it will compress the
data.

Checking old chunks that are good candidates to compress:

```sql
SELECT show_chunks('conditions', older_than => INTERVAL '3 days');
```

You can decompress manually a chunk with the following command:

```sql
SELECT decompress_chunk_named(chunk_name::varchar) 
FROM timescaledb_information.chunks WHERE is_compressed limit 1;
```

# GraphQL Mutations

On GraphQL, the convention for operations that is writing data is use mutations.

We need to map those mutations for compress and decompress a chunk. To
accomplish that, we need to take a look on how hasura types works.

## Hasura types

Hasura can use some custom types that comes from table structures.

I couldn't find a simple way to wrap this without using a table, so, I'll easily
get the structure of the table calling the function with limit 0:

## Compress chunk mutation


```sql
CREATE TABLE compressed_chunk AS
SELECT compress_chunk((c.chunk_schema ||'.' ||c.chunk_name)::regclass)
FROM   timescaledb_information.chunks c
WHERE  NOT c.is_compressed limit 0;
```

Hasura needs some function to be tracked as mutation. In this case, let's create the function to just rewrap the default `compress_chunk` from timescale extension. 

Now, we can return the "compressed_chunk" in our function that will compress the chunk:

```sql
CREATE OR REPLACE FUNCTION compress_chunk_named(varchar) returns setof compressed_chunk AS $$
  SELECT compress_chunk((c.chunk_schema ||'.' ||$1)::regclass)
  FROM   timescaledb_information.chunks c
  WHERE  NOT c.is_compressed
  AND    c.chunk_name = $1 limit 1
$$ LANGUAGE SQL VOLATILE;
```

> Note that the function add an extra where clause to not compress what is already compressed.

## Decompress chunk mutation

We'll need a similar function for the decompression:

```sql
CREATE OR replace FUNCTION decompress_chunk_named(varchar) returns setof compressed_chunk AS $$
  SELECT decompress_chunk((c.chunk_schema ||'.' ||$1)::regclass)
  FROM   timescaledb_information.chunks c
  WHERE  c.is_compressed
  AND    c.chunk_name = $1 limit 1
$$ LANGUAGE SQL VOLATILE;
```

Now, the next step is jump into hasura cloud and connect the database as a new
data source.


In the data panel, after setting up the postgresql URI of you database, you can
easily track each function as a query or mutation. Here is an example of `compress_chunk_named` function:

<img width="617" alt="Screen Shot 2021-06-16 at 15 23 48" src="https://user-images.githubusercontent.com/15484/122272819-27fa8a80-ceb7-11eb-93de-ddf678acbc2a.png">


In our case, the subscription goes to the `chunks_with_compression` and here is what it looks like:

<img width="701" alt="Screen Shot 2021-06-16 at 15 25 20" src="https://user-images.githubusercontent.com/15484/122273065-6bed8f80-ceb7-11eb-8233-58d9fcccb2d1.png">


You should also track `decompress_chunk_named` and `compress_chunk_named` as GQL mutations with a single argument.

## Setup application

Create a `.env` file with your hasura key:

```bash
HASURA_ADMIN_SECRET=...
HASURA_URI=wss://<your-project>.hasura.app/v1/graphql
```

Install all dependencies before run the project:

```bash
yarn install
```

## Exploring the React Components

This app was built with `create-react-app` and this is the most easy way to
setup the app.

The third party libraries added was only:

1. [Apollo][apollo-react] to get a websocket client.
2. [Timescale Styles][timescale-styles] to get some default styles from Timescale branding.

### Setting up ApolloClient connection

The first step is get the Apollo client up and connecting to the Hasura cloud.

> Note that you should have the `.env` file properly configured to make it work.

```javascript
const createApolloClient = () => {
  return new ApolloClient({
    link: new WebSocketLink({
      uri: process.env.HASURA_URI,
      options: {
        reconnect: true,
        connectionParams: {
          headers: {
            'x-hasura-admin-secret':
              process.env.HASURA_ADMIN_SECRET,
          },
        },
      },
    }),
    cache: new InMemoryCache(),
  });
};
```

In the main `App` we have:

```javascript
function App() {
  const client = createApolloClient();

  return (
    <ApolloProvider client={client} className="App">
      <Subscription />
    </ApolloProvider>
  );
}

export default App;
```

Note that we have a `Subscription` component, that is where we subscribe to our 
`chunks_with_compression` view that we mapped as a resource on Hasura Cloud.


```javascript
const Subscription = () => {
  const { data } = useSubscription(
    gql`
      subscription Chunks {
        chunks_with_compression {
          hypertable_name
          chunk_name
          range_start
          range_end
          before_compression_total_bytes
          after_compression_total_bytes
        }
      }
    `
  );
}
```

We need to have some state to control when we receive the chunks. React uses
states to pass information between components and if any data changes, it will
automatically refresh the components through `useEffect` hook.

```javascript
  const [chunks, setChunks] = useState([]);

  useEffect(() => {
    if (data && data.chunks_with_compression) {
      setChunks(data.chunks_with_compression);
    }
  }, [data]);

  return (<svg id="chunks" width="90vw" height="75vh" fill="none"
            className="ts-compression__inner__chunks__cards-wrapper"
            xmlns="http://www.w3.org/2000/svg"
          >
            {chunks.length > 0 &&
              chunks
                .filter((chunk) => chunk.hypertable_name === 'conditions')
                .map((chunk, index) => (
                  <Chunk {...chunk} key={index} />
                ))}
          </svg>);
};

export default Subscription;
```

This is the minimal example and we evolved to exchange several states and
enhance with more functionalities.

In the `Chunk`, it's possible to build the logic of the component and think about
the compression visualization and how to explore it.

Here is a small example of what the final component returns:

```javascript
  return (
    <>
      <circle
        r={radioSize}
        cx={circlePosition.cx}
        cy={circlePosition.cy}
        strokeWidth="2"
        id={chunk_name}
        ref={ref}
        onClick={handleClick}
      />
    </>
  );
```

We have two main aspects of the chunk visualization, the position and the size.

Let's start with the size, that is defined by the `radioSize`. It will be a
state that will depend on the sum of all uncompressed data. By default we start
with 24 pixels.

The first think we need to get is some proportions of the screen. We created a
`spreadFactor` that can be defined as the square root of the size of the screen
divided by the total bytes uncompressed. We split this value by the number of
chunks to know the distance between them.

```javascript
  const [spreadFactor, setSpreadFactor] = useState(() => {
    if (typeof window !== undefined){
      const pixelsPerByte = (window.innerWidth * window.innerHeight) / totalBytesUncompressed;
      return Math.sqrt(pixelsPerByte) / totalChunks;
    }
  }
```

With spreadFactor in place, we can now think about how to size every circle. The
first thing is create a new state to set the radioSize.

```javascript
const [radioSize, setRadioSize] = useState(24);
```

The next step is create a new hook to resize it based in the total bytes.
When the `after_compression_total_bytes` is available, it will use this
as the size factor otherwise it gets from the compressed size.


```javascript
useEffect(() => {
  const calcRadioSize =
    setRadioSize(() => {
      if (after_compression_total_bytes)
        return after_compression_total_bytes * spreadFactor;
      return before_compression_total_bytes * spreadFactor;
    });
}, [isCompressed, biggestChunk]);
```

The objective is that the entire area represents the full area of the
uncompressed data. So, here is how we break down the formula for choosing the
proper position for X and Y and spread the circles in the screen.

We start our thought with getting the sense of a squared space. With squared
elements. So, given the total amount of chunks, we can square root it to get the
size of or circles matrix:

```javascript
const squaredTotalChunks = Math.sqrt(totalChunks);
```

The `svg` element has an `id` named `chunks` and we can use such info to get the
properties of the element in the screen and better distribute the circles.
We'll use independent factors for width and height.

Let's start with the simple one that is width:

```javascript
const circlePosition = document.getElementById('chunks').getBoundingClientRect();
const widthRatio = circlePosition.width / squaredTotalChunks;
```
As the height is smaller than the width, we need to compensate it to keep the
"square" proportion.

```javascript
const compensationRatio =  circlePosition.width / circlePosition.height;
const heightRatio = compensationRatio * (circlePosition.height / squaredTotalChunks);
```

The index refers to what chunk is iterating over loop, so, it will be used as a
step to get into a fair distribution of the space.

```javascript
const cx = (widthRatio * ((index+1) % squaredTotalChunks));
const cy = (heightRatio * ((index+1) / squaredTotalChunks));

setCirclePosition({ cx, cy});
```

Now, that you got an understanding of all steps to build the calculate the size,
let's wrap it into a function that can be used in the `useEffect` hook.

```javascript
const handleCirclePosition = () => {
  const squaredTotalChunks = Math.sqrt(totalChunks);

  const circlePosition = document.getElementById('chunks').getBoundingClientRect();

  const compensationRatio =  circlePosition.width  / circlePosition.height;
  const widthRatio = circlePosition.width / squaredTotalChunks;
  const heightRatio = compensationRatio * (circlePosition.height / squaredTotalChunks);

  const cx = (widthRatio * ((index+1) % squaredTotalChunks));
  const cy = (heightRatio * ((index+1) / squaredTotalChunks));

  setCirclePosition({ cx, cy});
};
```

Now, it's time to use the sizing function in the `useEffect` hook when it
starts.

```javascript
useEffect(handleCirclePosition, []);
```

When it finds a new biggest chunk or the chunk changes the state, we should also
recalculate it:

```javascript
useEffect(handleCirclePosition, [isCompressed, biggestChunk]);
```

### Chunk events

The next step is to map the events to interact with the chunk. When clicking in the chunk, we want to compress or decompress.
If we mouse over the circle, it should plot some card with the info.

#### Click in the chunk to compress/decompress

Now it’s time to interact with the chunk and check more details of the handleClick function. If the chunk is compressed we can decompress or make the inverse operation case it’s decompressed.

Let’s start by declaring the mutation to compress the chunk:

```javascript
const COMPRESS_CHUNK = gql`
  mutation ($chunk: String!) {
    compress_chunk_named(args: { arg_1: $chunk }) {
      compress_chunk
    }
  }
`;
```
As you can see, the mutation receives an argument that is the `chunk_name` from the context. Now we can create a similar structure to also decompress the chunk:

```javascript
const DECOMPRESS_CHUNK = gql`
  mutation ($chunk: String!) {
    decompress_chunk_named(args: { arg_1: $chunk }) {
      compress_chunk
    }
  }
`;
```

Depending the state of the chunk, we’re going to choose the operation to compress or decompress, so, our mutation will be initialized with the proper GraphQL statement:


```javascript
const [mutation] = useMutation( isCompressed ? DECOMPRESS_CHUNK : COMPRESS_CHUNK);
```

Then, when we handle the click, we just execute the mutation binding the actual chunk name in the context. In this case we’re suppressing the front end details that shows a modal when it’s compressing.

```javascript
const handleClick = () => { mutation( { variables: { chunk: chunk_name } }); };
```

#### Mouse over the chunk to see details

Apart from having the chunk available on the screen and clicking through the circles, we also want to get more information about the sizing if we mouse hover it. So, let’s create a React hook to change the hover state:

```javascript
import useHover from '../hooks/useOnHover';
```

Creating the hook to control the hovering state of each independent chunk.

```javascript
import { useState, useEffect, useRef } from 'react';
const useHover = () => {
  const ref = useRef();
  const [hovered, setHovered] = useState(false);
  const enter = () => setHovered(true);
  const leave = () => setHovered(false);
  useEffect(() => {
    const el = ref.current; // cache external ref value for cleanup use
    if (el) {
      el.addEventListener('mouseenter', enter);
      el.addEventListener('mouseover', enter);
      el.addEventListener('mouseleave', leave);
      return () => {
        el.removeEventListener('mouseenter', enter);
        el.removeEventListener('mouseover', enter);
        el.removeEventListener('mouseleave', leave);
      };
    }
  }, []);
  return [ref, hovered];
};
export default useHover;
```

And now we can just use it as a state for the actual Chunk component:


```javascript
const [ref, hovered] = useHover();
```


Now, the hovered variable changes the we can push a new state to handleCardInfo and useEffect to show the actual chunk information in the informative card:


```javascript
  useEffect(() => {
    if (hovered)
      return handleCardInfo({
        chunk_name,
        before_compression_total_bytes,
        after_compression_total_bytes,
        range_start,
        range_end,
        cardPosition,
      });
    return handleCardInfo({});
  }, [hovered]);
```

Keep in mind that the InformationCard is a simple component that receives the data via state and expose the values closer to the hovered element.

```javascript
const CardInfo = ({
  chunk_name,
  before_compression_total_bytes,
  after_compression_total_bytes,
  cardPosition,
}) => {
  const getCompressionRatio = (before, after) => {
    if (!after) {
      return 0;
    }
    return (before / after).toFixed(2);
  };

  const compressionRatio = getCompressionRatio(
    before_compression_total_bytes,
    after_compression_total_bytes
  );

  const { top, bottom, left, right } = cardPosition || {};

  return (
    <div
      className="ts-compression__inner__info"
      style={{
        position: 'fixed',
        top: `calc(${top}px - 20px)`,
        right: `calc(${right}px + 80px)`,
        left: `calc(${left}px + 80px)`,
        bottom: `calc(${bottom}px - 20px)`,
      }}
    >
      <div className="ts-compression__inner__info--content">
        <h4>{chunk_name}</h4>
        <h4>Before Compression</h4>
        <Count
          suffix=" bytes"
          start={before_compression_total_bytes}
          end={before_compression_total_bytes}
        />
        <h4>After Compression</h4>
        <Count
          suffix=" bytes"
          start={before_compression_total_bytes}
          end={after_compression_total_bytes || 0}
        />
        <Count
          prefix="Compression Ratio: "
          end={compressionRatio}
          decimals={2}
        />
      </div>
    </div>
  );
};

export default CardInfo;
```

Now, we can change the subscription to also include the CardInfo visible when the user is hovering a chunk:

```javascript
<div className={cardInfoClasses}>
   <CardInfo {...cardInfo} />
</div>
```

And the cardInfoClasses can be toggling the CSS class names that controls if the card is showing up or not. If the cardInfo is an empty object it means nobody is hovering over it.

```javascript
const cardInfoClasses = classNames({
  'active':  Object.keys(cardInfo).length > 0,
});
```

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

[apollo-react]: https://www.apollographql.com/docs/react/
