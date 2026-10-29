/**
 * 9Router JavaScript/TypeScript Client
 * Auto-integration for chat, images, embeddings, web search, TTS/STT
 *
 * Usage:
 *   import { NineRouterClient } from './9router-client.js';
 *   const client = new NineRouterClient();
 *   const response = await client.chat('Hello, world!');
 */

export interface Model {
  id: string;
  owned_by: string;
  kind?: string;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string;
  tool_calls?: any[];
  tool_call_id?: string;
}

export interface ChatOptions {
  model?: string;
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
}

export interface EmbeddingOptions {
  model?: string;
}

export interface ImageOptions {
  model?: string;
  n?: number;
  size?: string;
}

export interface TTSOptions {
  model?: string;
  voice?: string;
  format?: string;
}

export interface STTOptions {
  model?: string;
  language?: string;
}

export interface SearchOptions {
  model?: string;
  max_results?: number;
}

export interface FetchOptions {
  model?: string;
  max_characters?: number;
}

export class NineRouterClient {
  private baseUrl: string;
  private apiKey: string | undefined;
  private timeout: number;

  constructor(options: {
    baseUrl?: string;
    apiKey?: string;
    timeout?: number;
  } = {}) {
    this.baseUrl = options.baseUrl || process.env.NINEROUTER_URL || 'http://localhost:20128';
    this.apiKey = options.apiKey || process.env.NINEROUTER_KEY;
    this.timeout = options.timeout || 30000;
  }

  private async request(method: string, endpoint: string, body?: any): Promise<any> {
    const url = `${this.baseUrl}/v1${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`9Router ${response.status}: ${error}`);
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  // ===== Health =====
  async health(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/health`, {
        signal: AbortSignal.timeout(5000),
      });
      const data = await response.json();
      return data.ok === true;
    } catch {
      return false;
    }
  }

  // ===== Models =====
  async listModels(kind: string = ''): Promise<Model[]> {
    const endpoint = kind ? `/models/${kind}` : '/models';
    const data = await this.request('GET', endpoint);
    return data.data || [];
  }

  // ===== Chat =====
  async chat(messages: ChatMessage[], options: ChatOptions = {}): Promise<any> {
    const payload = {
      model: options.model || 'auto',
      messages,
      temperature: options.temperature ?? 0.7,
      max_tokens: options.max_tokens,
      stream: options.stream || false,
    };

    if (options.stream) {
      return this.streamChat(payload);
    }
    return this.request('POST', '/chat/completions', payload);
  }

  async *streamChat(payload: any): AsyncGenerator<string, void, unknown> {
    const url = `${this.baseUrl}/v1/chat/completions`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`Stream failed: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') return;
          try {
            const chunk = JSON.parse(data);
            const delta = chunk.choices?.[0]?.delta;
            if (delta?.content) {
              yield delta.content;
            }
          } catch {}
        }
      }
    }
  }

  async chatSimple(prompt: string, options: ChatOptions = {}): Promise<string> {
    const response = await this.chat([{ role: 'user', content: prompt }], options);
    return response.choices?.[0]?.message?.content || '';
  }

  // ===== Embeddings =====
  async embed(texts: string[], options: EmbeddingOptions = {}): Promise<number[][]> {
    const data = await this.request('POST', '/embeddings', {
      model: options.model || 'auto',
      input: texts,
    });
    return data.data.map((d: any) => d.embedding);
  }

  // ===== Image Generation =====
  async generateImage(prompt: string, options: ImageOptions = {}): Promise<string[]> {
    const data = await this.request('POST', '/images/generations', {
      model: options.model || 'auto',
      prompt,
      n: options.n || 1,
      size: options.size || '1024x1024',
    });
    return data.data.map((d: any) => d.url);
  }

  // ===== Text-to-Speech =====
  async tts(text: string, options: TTSOptions = {}): Promise<ArrayBuffer> {
    const url = `${this.baseUrl}/v1/audio/speech`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        model: options.model || 'auto',
        input: text,
        voice: options.voice || 'alloy',
        format: options.format || 'mp3',
      }),
    });

    if (!response.ok) {
      throw new Error(`TTS failed: ${response.statusText}`);
    }

    return response.arrayBuffer();
  }

  // ===== Speech-to-Text =====
  async stt(audioFile: File | Blob, options: STTOptions = {}): Promise<string> {
    const formData = new FormData();
    formData.append('file', audioFile);
    formData.append('model', options.model || 'auto');
    formData.append('language', options.language || 'pt');

    const url = `${this.baseUrl}/v1/audio/transcriptions`;
    const headers: Record<string, string> = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`STT failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.text;
  }

  // ===== Web Search =====
  async webSearch(query: string, options: SearchOptions = {}): Promise<any[]> {
    const data = await this.request('POST', '/web/search', {
      model: options.model || 'auto',
      query,
      max_results: options.max_results || 10,
    });
    return data.results || [];
  }

  // ===== Web Fetch =====
  async webFetch(urls: string[], options: FetchOptions = {}): Promise<any[]> {
    const data = await this.request('POST', '/web/fetch', {
      model: options.model || 'auto',
      urls,
      max_characters: options.max_characters || 3000,
    });
    return data.results || [];
  }

  // ===== Auto-Routing (Combo Models) =====
  async autoChat(prompt: string, options: ChatOptions = {}): Promise<string> {
    return this.chatSimple(prompt, { ...options, model: 'combo/general' });
  }

  async autoSearch(query: string, options: SearchOptions = {}): Promise<any[]> {
    return this.webSearch(query, { ...options, model: 'combo/search' });
  }
}

// ===== Singleton / Convenience =====
let defaultClient: NineRouterClient | null = null;

export function getClient(): NineRouterClient {
  if (!defaultClient) {
    defaultClient = new NineRouterClient();
  }
  return defaultClient;
}

export async function chat(prompt: string, options?: ChatOptions): Promise<string> {
  return getClient().autoChat(prompt, options);
}

export async function search(query: string, options?: SearchOptions): Promise<any[]> {
  return getClient().autoSearch(query, options);
}

export async function embed(texts: string[], options?: EmbeddingOptions): Promise<number[][]> {
  return getClient().embed(texts, options);
}

export async function generateImage(prompt: string, options?: ImageOptions): Promise<string[]> {
  return getClient().generateImage(prompt, options);
}

export async function tts(text: string, options?: TTSOptions): Promise<ArrayBuffer> {
  return getClient().tts(text, options);
}

// ===== Demo =====
if (import.meta.main) {
  const client = new NineRouterClient();

  console.log('=== 9Router Client Demo ===\n');

  const healthy = await client.health();
  console.log(`Health: ${healthy ? 'OK' : 'FAIL'}`);

  if (healthy) {
    const models = await client.listModels();
    console.log(`\nAvailable models (${models.length}):`);
    models.slice(0, 5).forEach(m => console.log(`  - ${m.id} (${m.owned_by})`));

    console.log('\n--- Chat Test ---');
    try {
      const response = await client.autoChat('Olá! Responda em português: qual a capital do Brasil?');
      console.log(`Response: ${response}`);
    } catch (e) {
      console.error('Chat error:', e);
    }

    console.log('\n--- Web Search Test ---');
    try {
      const results = await client.autoSearch('GitHub Copilot app download Windows');
      results.slice(0, 3).forEach(r => console.log(`  - ${r.title}: ${r.url}`));
    } catch (e) {
      console.error('Search error:', e);
    }
  } else {
    console.log('\n9Router not running. Start with: npx @decolua/9router');
  }
}