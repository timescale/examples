import React from 'react';
import { useMutation, gql } from '@apollo/client';
import './buttons.scss';
import classNames from 'classnames';

const COMPRESS_CHUNK = gql`
mutation ($chunk: String!) {
  compress_chunk_named(args: {arg_1: $chunk}) {
    compress_chunk
  }
}
`;

const DECOMPRESS_CHUNK = gql`
  mutation ($chunk: String!) {
    decompress_chunk_named(args: { arg_1: $chunk }) {
      compress_chunk
    }
  }
`;

const ADD_DATA = '';

const mutationsMap = {
  compress: COMPRESS_CHUNK,
  decompress: DECOMPRESS_CHUNK,
  addData: ADD_DATA,
};

function Button({ jobComplete, setLoadModal, isCompressed, chunkName }) {
  const buttonType = isCompressed ? 'decompress' : isCompressed  === undefined ? 'addData' : 'compress';
  const btnClassNames = classNames({'btn': true, [`btn__${buttonType}`]: true, [`btn__${buttonType}--disabled`]: jobComplete});
  const [mutation] = useMutation(mutationsMap[buttonType]);
  const mutationVariables = chunkName ? { variables: {chunk: chunkName} } : {variables: {}};
  const label = isCompressed !== undefined ? buttonType.toUpperCase() : 'ADD DATA';


  const handleClick = () => {
    setLoadModal(true);
    mutation(mutationVariables);
  }

  return <button className={btnClassNames} onClick={() => handleClick()}>{label}</button>;
}

export default Button;
