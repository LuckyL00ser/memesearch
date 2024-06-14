import "./App.css";
import { Footer } from "./components/Footer";
import { Header } from "./components/Header";
import { ImageGrid } from "./components/ImageGrid";
import Searchbar from "./components/Searchbar";
import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query'
import { PageProvider } from "./providers/PageContext";
import { MemesProvider } from "./providers/MemesContext";
import ProgressBar from "./components/ProgressBar";

const queryClient = new QueryClient()


function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <PageProvider>
        <MemesProvider>
          <div className="min-h-screen bg-gradient-to-br from-indigo-900 to-stone-900 text-white flex flex-col items-center">
            <Header />
            <main className="flex-1 w-full max-w-3xl p-4">
              <div className="mb-4">
                <ProgressBar/>
                <Searchbar />
              </div>
              <ImageGrid />
            </main>
            <Footer />
          </div>
        </MemesProvider>
      </PageProvider>
    </QueryClientProvider>
  );
}

export default App;
