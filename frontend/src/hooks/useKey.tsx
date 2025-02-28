import { useEffect } from "react";

const useEscapeKey = (triggerFunc: () => void, key:string) => {
  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === key) {
        triggerFunc();
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [triggerFunc]);
};

export default useEscapeKey;