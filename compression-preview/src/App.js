import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';
import Subscription from './Subscription';
import { WebSocketLink } from '@apollo/client/link/ws';
import './App.css';

const createApolloClient = () => {
  return new ApolloClient({
    link: new WebSocketLink({
      uri: 'wss://fleet-bunny-18.hasura.app/v1/graphql',
      options: {
        reconnect: true,
        connectionParams: {
          headers: {
            'x-hasura-admin-secret':
              process.env.REACT_APP_X_HASURA_ADMIN_SECRET,
          },
        },
      },
    }),
    cache: new InMemoryCache(),
  });
};


function App() {
  const client = createApolloClient();

  return (
    <ApolloProvider client={client} className="App">
      <Subscription />
    </ApolloProvider>
  );
}

export default App;
