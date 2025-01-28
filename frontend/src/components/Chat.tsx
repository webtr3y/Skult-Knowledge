import React, { useState, useCallback, useRef, useEffect } from 'react';
import {
  Box,
  Input,
  Button,
  VStack,
  Text,
  useColorMode,
  BoxProps,
  useToast,
  UseToastOptions,
} from '@chakra-ui/react';

// Types
interface Message {
  id: string;
  text: string;
  isUser: boolean;
  suggestedActions?: string[];
  timestamp: number;
}

interface ChatResponse {
  response: string;
  suggested_actions?: string[];
}

interface ChatProps extends Omit<BoxProps, 'children'> {
  onSend?: (message: string) => void;
}

// Constants
const TOAST_CONFIG: UseToastOptions = {
  title: 'Error',
  description: 'Failed to send message',
  status: 'error',
  duration: 5000,
  isClosable: true,
  position: 'top-right',
} as const;

export const Chat = React.memo(({ onSend, ...props }: ChatProps): JSX.Element => {
  // State
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Hooks
  const { colorMode } = useColorMode();
  const toast = useToast();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll effect
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Message handlers
  const createMessage = useCallback((
    text: string,
    isUser: boolean,
    suggestedActions?: string[]
  ): Message => ({
    id: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
    text,
    isUser,
    suggestedActions,
    timestamp: Date.now(),
  }), []);

  const handleError = useCallback((error: unknown) => {
    const errorMessage = error instanceof Error ? error.message : 'An error occurred';
    console.error('Chat error:', errorMessage);
    toast(TOAST_CONFIG);
    setMessages(prev => [
      ...prev,
      createMessage('Sorry, an error occurred while processing your message.', false)
    ]);
  }, [toast, createMessage]);

  // API interaction
  const sendMessage = useCallback(async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    try {
      setIsLoading(true);
      const userMessage = createMessage(trimmedInput, true);
      setMessages(prev => [...prev, userMessage]);
      setInput('');

      onSend?.(trimmedInput);

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ message: trimmedInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = (await response.json()) as ChatResponse;
      
      setMessages(prev => [
        ...prev,
        createMessage(data.response, false, data.suggested_actions)
      ]);
    } catch (error) {
      handleError(error);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, createMessage, handleError, onSend]);

  // Event handlers
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  }, []);

  const handleKeyPress = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void sendMessage();
    }
  }, [sendMessage]);

  const handleSuggestedAction = useCallback((action: string) => {
    setInput(action);
  }, []);

  // Render
  return (
    <Box
      maxW="600px"
      mx="auto"
      p={4}
      bg={colorMode === 'dark' ? 'gray.800' : 'gray.100'}
      borderRadius="md"
      fontFamily="monospace"
      position="relative"
      role="region"
      aria-label="Chat interface"
      {...props}
    >
      <VStack spacing={4} align="stretch" h="600px">
        <Box
          flex={1}
          overflowY="auto"
          p={2}
          bg={colorMode === 'dark' ? 'gray.700' : 'white'}
          borderRadius="md"
          role="log"
          aria-live="polite"
        >
          {messages.map((msg) => (
            <Box 
              key={msg.id}
              mb={4}
              data-testid={`message-${msg.id}`}
              role="article"
            >
              <Text
                color={msg.isUser ? 'green.400' : 'blue.400'}
                fontWeight="bold"
                as="span"
              >
                {msg.isUser ? '> You:' : '> SEI Agent:'}
              </Text>
              <Text pl={4} as="p">{msg.text}</Text>
              {msg.suggestedActions?.length > 0 && (
                <Box pl={4} mt={2} role="group" aria-label="Suggested actions">
                  {msg.suggestedActions.map((action, idx) => (
                    <Button
                      key={`${msg.id}-action-${idx}`}
                      size="sm"
                      variant="outline"
                      mr={2}
                      mb={2}
                      onClick={() => handleSuggestedAction(action)}
                      data-testid={`suggested-action-${idx}`}
                      isDisabled={isLoading}
                      aria-label={`Use suggestion: ${action}`}
                    >
                      {action}
                    </Button>
                  ))}
                </Box>
              )}
            </Box>
          ))}
          <div ref={messagesEndRef} />
        </Box>
        <Box role="form">
          <Input
            value={input}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="> Type your message..."
            fontFamily="monospace"
            aria-label="Chat input"
            data-testid="chat-input"
            isDisabled={isLoading}
            autoComplete="off"
            spellCheck="false"
          />
        </Box>
      </VStack>
    </Box>
  );
});

Chat.displayName = 'Chat';

export default Chat; 