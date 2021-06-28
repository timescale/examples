import React, { useState, useEffect } from 'react';
import classNames from 'classnames';
import useHover from '../hooks/useOnHover';
import { useMutation, gql } from '@apollo/client';

const COMPRESS_CHUNK = gql`
  mutation ($chunk: String!) {
    compress_chunk_named(args: { arg_1: $chunk }) {
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

function Chunk({
  after_compression_total_bytes,
  before_compression_total_bytes,
  biggestChunk,
  chunk_name,
  index,
  range_start,
  range_end,
  handleCardInfo,
  handleBiggestChunk,
  handleCompressingModal,
  screenDimensions,
  totalChunks,
  totalBytesUncompressed,
}) {
  const [ref, hovered] = useHover();

  const [isCompressed, setIsCompressed] = useState(
    after_compression_total_bytes !== null
  );

  const [loadModal, setLoadModal] = useState(true);

  const [radioSize, setRadioSize] = useState(24);

  const [cardPosition, setCardPosition] = useState({});

  const [spreadFactor, setSpreadFactor] = useState(() => {
    if (typeof window !== undefined){
      const pixelsPerByte = (window.innerWidth * window.innerHeight) / totalBytesUncompressed;
      return Math.sqrt(pixelsPerByte) / totalChunks;
    }
  }
);

  const [circlePosition, setCirclePosition] = useState({
    cx: 700,
    cy: 300,
  });

  const [mutation] = useMutation(
    isCompressed ? DECOMPRESS_CHUNK : COMPRESS_CHUNK
  );

  const circleClassNames = classNames(
    'ts-compression__inner__chunks__cards-wrapper__card',
    {
      'ts-compression__inner__chunks__cards-wrapper__card--compressed':
        isCompressed,
      'ts-compression__inner__chunks__cards-wrapper__card--decompressed':
        !isCompressed,
      'ts-compression__inner__chunks__cards-wrapper__card--hovered': hovered,
    }
  );

  const handleCirclePosition = () => {
    const squaredTotalChunks = Math.sqrt(totalChunks);

    const circlePosition = document.getElementById('chunks').getBoundingClientRect();

    const compensationRatio =  circlePosition.width  / circlePosition.height;
    const widthRatio = circlePosition.width / squaredTotalChunks;
    const heightRatio = compensationRatio * (circlePosition.height / squaredTotalChunks);

    const cx = 20 + ((widthRatio * ((index+1) % squaredTotalChunks)) * 0.97);
    const cy = 20 + ((heightRatio * ((index+1) / squaredTotalChunks)) * 0.5);

    setCirclePosition({ cx, cy});
  };

  const handleSpreadFactor = () =>
    setSpreadFactor(
      typeof window !== undefined &&
        Math.sqrt(
          (window.innerWidth * window.innerHeight) /
            totalBytesUncompressed
        ) / totalChunks
    );

  const handleClick = () => {
    setLoadModal(true);
    handleCompressingModal(true);
    mutation({ variables: { chunk: chunk_name } });
  };

  const getCardPosition = () => document.getElementById(chunk_name).getBoundingClientRect();

  useEffect(() => {
    setLoadModal(false);
    setIsCompressed(after_compression_total_bytes !== null);
  }, [after_compression_total_bytes, before_compression_total_bytes]);

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

  useEffect(() => {
    handleBiggestChunk({ chunk_name, before_compression_total_bytes });
  }, []);

  useEffect(() => {
    setRadioSize(() => {
      if (after_compression_total_bytes)
        return after_compression_total_bytes * spreadFactor;
      return before_compression_total_bytes * spreadFactor;
    });
    handleCirclePosition();
    setCardPosition(getCardPosition());
  }, [isCompressed, biggestChunk, totalChunks]);

  useEffect(() => {
    handleSpreadFactor();
  }, [totalBytesUncompressed]);

  useEffect(() => {
    handleCirclePosition();
  }, []);

  return (
    <>
      <circle
        cx={circlePosition.cx}
        cy={circlePosition.cy}
        r={radioSize}
        strokeWidth="2"
        id={chunk_name}
        ref={ref}
        className={circleClassNames}
        onClick={handleClick}
      />
    </>
  );
}

export default Chunk;
