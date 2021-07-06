import { useState, useEffect, useRef } from 'react';
const useHover = () => {
  const ref = useRef();
  const [hovered, setHovered] = useState(false);
  const enter = () => setHovered(true);
  const leave = () => setHovered(false);
  // eslint-disable-next-line consistent-return
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
