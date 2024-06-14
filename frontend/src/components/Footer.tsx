import { useMemo } from "react";
import { usePageContext } from "../providers/PageContext";

function range(size: number, startAt = 0) {
  // @ts-ignore
  return [...Array(size).keys()].map((i) => i + startAt);
}

export const Footer = () => {
  const { page, pagesCount, setPage } = usePageContext();

  const prevPage = () => {
    setPage(Math.max(page - 1, 0));
  };
  const nextPage = () => {
    setPage(Math.min(page + 1, pagesCount - 1));
  };

  const { begginingPages, currentPage, endPages } = useMemo(() => {
    let begginingPages : number[] = [];
    let currentPage : (number | string)[] = [];
    let endPages : number[] = [];

    //one continious section of page numbers
    if (pagesCount < 7 || pagesCount === 7 && ((page + 1 == 4) || page + 1 == pagesCount - 3)) begginingPages = range(pagesCount, 1);
    else {
      //too many pages required '...'
      //set [1,2,3] and [x-2, x-1, x]
      begginingPages = range(3, 1)
      endPages = range(3,pagesCount - 2)
      if(page + 1> 4 && page + 1 < pagesCount - 3){
        //current page not aligned to the beggining nor end
        currentPage = ['...', page + 1,'...']
      }else if (page + 1 === 4) {
        //current page aligned to beginning
        currentPage = [4, '...']
      }else if (page + 1 === pagesCount - 3) {
        //current page aligned to end
        currentPage = ['...',page + 1]
      }else {
        //current page within beggining or end
        currentPage = ['...']
      }
    }
    return {
      begginingPages,
      currentPage,
      endPages,
    };
  }, [page, pagesCount]);

  const renderPageIndicator = (renderPage: number | string) => {
    const dynamicClassName = "p-2 hover:bg-white/[.06] rounded bg-none border-none" + (renderPage === page + 1 ? " text-amber-800" : "")
    return (
      typeof(renderPage) === 'string' ?
      <span className={dynamicClassName}>{renderPage}</span> :
      <button
        className={dynamicClassName}
        onClick={() => setPage(renderPage - 1)}
      >
        {renderPage}
      </button> 
    );
  };

  return (
    <footer className="w-full py-4 bg-gray-900 flex justify-center">
      <div className="w-full max-w-3xl flex justify-between items-center px-4">
        <button
          disabled={page === 0}
          onClick={prevPage}
          className="px-4 py-2 bg-gray-800 enabled:hover:text-amber-800  rounded-lg"
        >
          prev
        </button>
        <div>
          {begginingPages.map(renderPageIndicator)}
          {currentPage.map(renderPageIndicator)}
          {endPages.map(renderPageIndicator)}
        </div>
        <button
          disabled={page === pagesCount - 1}
          onClick={nextPage}
          className="px-4 py-2 bg-gray-800 enabled:hover:text-amber-800 rounded-lg"
        >
          next
        </button>
      </div>
    </footer>
  );
};
