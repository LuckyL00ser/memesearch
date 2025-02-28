import { BASE_DATA_URL } from "../api";

interface IMemeRect {
  meme: Meme
  onClick: () => void
}

const MemeRect = ({ meme, onClick }: IMemeRect) => {
    // const separate_keywords = ['x']// meme.keywords.replace(/^\[|\]$/g, '').replace(/"|'/g, '').split(', ').join(' / ')
    return (
      <div onClick={onClick} className="group rounded-lg overflow-hidden cursor-pointer relative max-h-[200px]"> 
        <div className="absolute h-full w-full transform transition-all duration-300 bg-transparent group-hover:bg-black/[.8] z-10 flex items-center p-4">
          <span className="text-transparent group-hover:text-gray-300 font-bold">{meme.keywords}</span>
        </div>
        <img
          className="object-fill transform transition-transform duration-300 group-hover:scale-105 w-full"
          src={BASE_DATA_URL+meme.img_path}
          alt="meme"
        />
        {meme.meme_analyzed_at && <div title="[MEME analyzed]" className="z-20 absolute bottom-1 right-2">✅</div>}
      </div>
    );
  };
export default MemeRect;