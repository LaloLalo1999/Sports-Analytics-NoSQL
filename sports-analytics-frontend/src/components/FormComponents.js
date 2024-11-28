import {
  FormControl as ChakraFormControl,
  FormLabel as ChakraFormLabel,
  FormErrorMessage,
} from '@chakra-ui/react';

export const FormControl = ({ children, isRequired, isInvalid, error }) => (
  <ChakraFormControl isRequired={isRequired} isInvalid={isInvalid}>
    {children}
    {isInvalid && <FormErrorMessage>{error}</FormErrorMessage>}
  </ChakraFormControl>
);

export const FormLabel = ({ children }) => (
  <ChakraFormLabel>{children}</ChakraFormLabel>
); 