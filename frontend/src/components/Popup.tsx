import React from 'react';
import { BASE_DATA_URL } from '../api';
import useKey from '../hooks/useKey';

interface PopupProps {
  meme: Meme;
  onClose: () => void;
}


export const Popup: React.FC<PopupProps> = ({ meme, onClose }) => {
  useKey(onClose, 'Escape');

  return (
    <div className="fixed inset-0 flex items-center overflow-hidden justify-center bg-black bg-opacity-50 z-40">
      <div className="relative overflow-hidden max-h-[500px]  bg-black p-6 rounded-lg shadow-lg">
        <button
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
          onClick={onClose}
        >
          X
        </button>
        <div className="flex flex-col max-h-full overflow-hidden">
          <img className="shrink" src={BASE_DATA_URL+meme.img_path} alt="" />
          <div className='flex-1'>
            <h2 className="text-xl font-bold mb-4">Meme Details</h2>
            <p><strong>Created At:</strong>  {new Date(meme.file_created_at).toLocaleString()}</p>  
            <p><strong>Keywords:</strong> {meme.keywords}</p>
            <p><strong>Analyzed At:</strong> {meme.meme_analyzed_at??'<never>'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};