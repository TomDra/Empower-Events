import { Button, TextField, Typography, Container, Box } from "@mui/material";

export const speak = (text) => {
	if ('speechSynthesis' in window) {
	  const utterance = new SpeechSynthesisUtterance(text);
	  speechSynthesis.speak(utterance);
	} else {
	  console.error("Speech synthesis not supported in this browser.");
	}
  };