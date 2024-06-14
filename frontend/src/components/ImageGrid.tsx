import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
import { useMemesContext } from "../providers/MemesContext";

interface IMemeRect {
  meme: Meme;
}

const MemeRect = ({ meme }: IMemeRect) => {
  return (
    <div className="group rounded-lg overflow-hidden cursor-pointer relative max-h-[200px]">
      <div className="absolute h-full w-full transform transition-all duration-300 bg-black/[.3] group-hover:bg-transparent z-10 flex items-center p-4">
        <span className="text-transparent group-hover:text-amber-800">{meme.keywords}</span>
      </div>
      <img
        className="relative object-cover object-center transform transition-transform duration-300 group-hover:scale-105"
        src={'http://localhost:80/data'+meme.id}
        alt="meme"
      />
      {meme.meme_analyzed_at && <div title="[MEME analyzed]" className="z-20 absolute bottom-1 right-2">✅</div>}
    </div>
  );
};

export const ImageGrid = () => {
  const { memes } = useMemesContext();
  return (
    <section className="">
      <ResponsiveMasonry columnsCountBreakPoints={{ 350: 1, 750: 2, 900: 3 }}>
        <Masonry gutter="4px">
          {memes.map((m) => (
            <MemeRect meme={m} key={m.id} />
          ))}
        </Masonry>
      </ResponsiveMasonry>
    </section>
  );
};
