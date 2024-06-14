import { keepPreviousData, queryOptions } from "@tanstack/react-query";
import axios from "axios";

// Define the response types
interface PaginatedMemeResponse {
  results: Meme[];
  pages: number;
  page: number;
}

interface CollectionStatusResponse {
  total_count: number;
  unanalyzed_count: number;
  analyzed_count: number;
  progress: number;
}

// Define the base URL for your API
const BASE_URL = process.env.NODE_ENV === "production" ? "/api" : "http://localhost:80/api";

// Function to get paginated memes
const getMemes = async (
  query: string | null = null,
  page: number = 0,
  pageSize: number = 20
): Promise<PaginatedMemeResponse> => {
  try {
    const response = await axios.get<PaginatedMemeResponse>(
      `${BASE_URL}/memes`,
      {
        params: {
          query,
          page,
          page_size: pageSize,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching memes:", error);
    throw error;
  }
};

// Function to get the collection status
const getStatus = async (): Promise<CollectionStatusResponse> => {
  try {
    const response = await axios.get<CollectionStatusResponse>(
      `${BASE_URL}/memes/collection-status`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching collection status:", error);
    throw error;
  }
};

export const getMemesQuery = (searchTerm: string, page: number, page_size:number=20) => {
  return queryOptions({
    queryKey: ["getMemes", { searchTerm, page, page_size }],
    queryFn: () => getMemes(searchTerm, page, page_size),
    placeholderData: keepPreviousData,
    retry: 0
  });
}

export const getStatusQuery = (refetchInterval:number) => {
  return queryOptions({
    queryKey: ["getStatus"],
    queryFn: getStatus,
    retry: 0,
    refetchInterval: refetchInterval
  });
}
