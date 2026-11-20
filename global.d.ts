export {};
declare global {
  interface Window {
    kitsune: {
      health: () => Promise<{ ok: boolean; service: string }>;
    };
  }
}
