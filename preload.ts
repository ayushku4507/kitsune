import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("kitsune", {
  health: () => ipcRenderer.invoke("kitsune:health")
});
