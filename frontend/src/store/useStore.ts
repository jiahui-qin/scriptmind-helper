import { create } from 'zustand'

interface Store {
  scriptId: number | null
  setScriptId: (id: number) => void
}

export const useStore = create<Store>(set => ({
  scriptId: null,
  setScriptId: (id: number) => set({ scriptId: id }),
}))
