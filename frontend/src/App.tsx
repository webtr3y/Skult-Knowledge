import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  ChakraProvider,
  Box,
  VStack,
  Heading, 
  Container,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useToast,
  UseToastOptions,
  extendTheme,
  ThemeConfig,
} from '@chakra-ui/react';
import { Chat } from './components/Chat';
import axios from 'axios';

// Types
interface SentimentDistribution {
  positive: number;
  neutral: number;
  negative: number;
}

interface TrendData {
  mention_count: number;
  avg_engagement: number;
  mentions_per_hour: number;
  sentiment_distribution: SentimentDistribution;
}

interface TrendingTopic {
  topic: string;
  data: TrendData;
}

interface ApiResponse {
  trending_topics: TrendingTopic[];
}

// Constants
const POLLING_INTERVAL = 60000; // 1 minute

const ERROR_TOAST: UseToastOptions = {
  title: 'Error',
  description: 'Failed to fetch trending topics',
  status: 'error',
  duration: 5000,
  isClosable: true,
  position: 'top-right',
} as const;

// Theme configuration
const themeConfig: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: true,
};

const customTheme = extendTheme({
  config: themeConfig,
  styles: {
    global: (props: { colorMode: string }) => ({
      body: {
        bg: props.colorMode === 'dark' ? 'gray.800' : 'gray.50',
      },
    }),
  },
  components: {
    Heading: {
      baseStyle: {
        fontWeight: 'semibold',
      },
    },
  },
});

export const App = (): JSX.Element => {
  // State
  const [trendingTopics, setTrendingTopics] = useState<TrendingTopic[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [blockData, setBlockData] = useState(null);
  const [posts, setPosts] = useState([]);
  
  // Hooks
  const toast = useToast();

  // API interaction
  const fetchTrendingTopics = useCallback(async (): Promise<void> => {
    if (isLoading) return;

    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/trending/topics', {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = (await response.json()) as ApiResponse;
      setTrendingTopics(data.trending_topics);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      console.error('Error fetching trending topics:', errorMessage);
      setError(errorMessage);
      toast(ERROR_TOAST);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, toast]);

  useEffect(() => {
    axios.get('/api/blockchain/latest-block')
      .then(response => setBlockData(response.data))
      .catch(error => console.error('Error fetching block data:', error));
  }, []);

  useEffect(() => {
    axios.get('http://localhost:5000/posts')
      .then(response => setPosts(response.data))
      .catch(error => console.error('Error fetching posts:', error));
  }, []);

  // Polling effect
  useEffect(() => {
    const controller = new AbortController();

    const fetchData = async (): Promise<void> => {
      try {
        await fetchTrendingTopics();
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          return;
        }
        throw error;
      }
    };

    void fetchData();

    const intervalId = window.setInterval(() => {
      void fetchData();
    }, POLLING_INTERVAL);

    return () => {
      controller.abort();
      window.clearInterval(intervalId);
    };
  }, [fetchTrendingTopics]);

  // Memoized renderers
  const renderTrendingTopic = useCallback((topic: TrendingTopic): JSX.Element => (
    <Box
      key={topic.topic}
      p={6}
      borderWidth={1}
      borderRadius="lg"
      boxShadow="md"
      data-testid={`trending-topic-${topic.topic}`}
      role="article"
      aria-labelledby={`topic-heading-${topic.topic}`}
    >
      <Heading 
        size="md" 
        mb={4} 
        id={`topic-heading-${topic.topic}`}
      >
        #{topic.topic}
      </Heading>
      <SimpleGrid columns={2} spacing={4}>
        <Stat>
          <StatLabel>Mentions</StatLabel>
          <StatNumber>{topic.data.mention_count}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Engagement</StatLabel>
          <StatNumber>{topic.data.avg_engagement.toFixed(1)}</StatNumber>
          <StatHelpText>per mention</StatHelpText>
        </Stat>
      </SimpleGrid>
    </Box>
  ), []);

  const handleChatMessage = useCallback((message: string): void => {
    console.log('Chat message sent:', message);
    // Add any additional chat message handling here
  }, []);

  // Memoized error component
  const errorDisplay = useMemo(() => (
    error && (
      <Box 
        p={4} 
        bg="red.100" 
        color="red.700" 
        borderRadius="md"
        data-testid="error-message"
        role="alert"
      >
        {error}
      </Box>
    )
  ), [error]);

  return (
    <ChakraProvider theme={customTheme}>
      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          <Heading as="h1">SEI Network Analytics</Heading>
          <Tabs variant="enclosed" isLazy>
            <TabList>
              <Tab data-testid="trending-tab">Trending Topics</Tab>
              <Tab data-testid="chat-tab">Chat Assistant</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                {errorDisplay}
                {isLoading ? (
                  <Box 
                    p={4} 
                    textAlign="center" 
                    data-testid="loading-indicator"
                    role="status"
                    aria-label="Loading trending topics"
                  >
                    Loading...
                  </Box>
                ) : (
                  <SimpleGrid 
                    columns={{ base: 1, md: 2, lg: 3 }} 
                    spacing={6}
                    data-testid="trending-topics-grid"
                    role="feed"
                    aria-label="Trending topics"
                  >
                    {trendingTopics.map(renderTrendingTopic)}
                  </SimpleGrid>
                )}
              </TabPanel>
              <TabPanel>
                <Chat onSend={handleChatMessage} />
              </TabPanel>
            </TabPanels>
          </Tabs>
          <Heading as="h2">Latest Block Information</Heading>
          {blockData ? (
            <pre>{JSON.stringify(blockData, null, 2)}</pre>
          ) : (
            <p>Loading...</p>
          )}
          <Heading as="h2">Posts</Heading>
          <ul>
            {posts.map(post => (
              <li key={post.id}>{post.title}</li>
            ))}
          </ul>
        </VStack>
      </Container>
    </ChakraProvider>
  );
};

export default App; 