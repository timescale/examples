import React from 'react';

import Count from './count';

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
          end={before_compression_total_bytes || 0}
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
