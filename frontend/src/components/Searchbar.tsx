import React, { useState, useCallback, useEffect } from 'react';
import useDebounce from '../hooks/debounceHook';
import { useQuery } from '@tanstack/react-query';
import { getMemesQuery } from '../api';
import { useMemesContext } from '../providers/MemesContext';
import { usePageContext } from '../providers/PageContext';

const Searchbar: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const debouncedSearchTerm = useDebounce<string>(searchTerm, 500);
  const {setMemes} = useMemesContext()
  const {page, setPage, setPagesCount} = usePageContext()

  const { isPending, isFetching, isError, error, data } = useQuery(getMemesQuery(debouncedSearchTerm, page))
  useEffect(()=>{
    setMemes(data?.results || [])
    setPagesCount(data?.pages || 0)
  },[data])
//   if (isPending) return 'Loading...'

//   if (error) return 'An error has occurred: ' + error.message

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };
  const dynamicInputClass = "w-full p-3 rounded-full  border border-gray-700 placeholder-gray-500 text-white" + (isFetching ? ' bg-gray-800' : ' bg-gray-800/[.5]')

  return (
    <div className='w-full relative'>
      {
       isFetching &&  <div className="absolute w-full h-full flex items-center justify-end pr-6" >
       <div className='animate-spin h-5 w-5 flex items-center'>.</div>
     </div>
      }
        <input
        type="text"
        // disabled={isFetching}
        value={searchTerm}
        onChange={handleChange}
        placeholder="Search your meme.."
        className={dynamicInputClass}
      />
    </div>
    
  );
};

export default Searchbar;
