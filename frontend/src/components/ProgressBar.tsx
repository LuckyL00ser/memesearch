import { useQuery } from "@tanstack/react-query";
import { getStatusQuery } from "../api";

const ProgressBar: React.FC = () => {
    const { data, error, isLoading } = useQuery(getStatusQuery(15000));
  
    if (isLoading) {
      return <div>Loading...</div>;
    }
  
    if (error) {
      return <div>Error loading progress</div>;
    }
  
    const progress = data?.progress ? parseInt(String(data.progress * 10000))/100.0 : 0;
  
    return (
      <div className="w-full bg-gray-200/[.3] rounded-full h-6 flex justify-center relative">
        <div className="z-10">
            {progress}%
        </div>
        <div
          className="bg-indigo-600 h-6 rounded-full transition-all duration-500 absolute top-0 left-0"
          style={{ width: `${progress}%` }}
        >
        </div>
      </div>
    );
  };
  
  export default ProgressBar;