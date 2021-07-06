import React from 'react';
import CountUp from 'react-countup';
function Count({
  start = 0,
  end,
  prefix,
  suffix,
  duration = .5,
  decimals = 0,
}) {
  
  return (
    <p>
      <CountUp
        start={start}
        end={end !== 0 && end > 50000 ? end - 5000 : end}
        duration={duration}
        separator=","
        decimals={decimals}
        prefix={prefix}
        suffix={suffix}
        useEasing
      />
    </p>
  );
}

export default Count;
