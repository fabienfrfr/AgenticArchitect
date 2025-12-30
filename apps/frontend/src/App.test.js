import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AgenticArchitectDashboard from './App';
import axios from 'axios';

jest.mock('mermaid', () => ({
    initialize: jest.fn(),
    run: jest.fn(),
    render: jest.fn(),
}));

jest.mock('axios');

describe('AgenticArchitect Dashboard Tests', () => {

    test('updates requirements input on change', () => {
        render(<AgenticArchitectDashboard />);
        const textarea = screen.getByPlaceholderText(/Enter your project requirements/i);
        fireEvent.change(textarea, { target: { value: 'Build a RAG system' } });
        expect(textarea.value).toBe('Build a RAG system');
    });
});