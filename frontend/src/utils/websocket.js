class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.listeners = {
      open: [],
      close: [],
      message: [],
      error: [],
    };
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log("WebSocket connected");
        this.reconnectAttempts = 0;
        this.listeners.open.forEach((callback) => callback());
      };

      this.ws.onclose = () => {
        console.log("WebSocket disconnected");
        this.listeners.close.forEach((callback) => callback());
        this.attemptReconnect();
      };

      this.ws.onmessage = (event) => {
        // Handle both text and binary messages
        if (event.data instanceof ArrayBuffer) {
          console.log("WebSocket binary message received:", event.data.byteLength, "bytes");
        } else {
          console.log("WebSocket message received:", event.data);
        }
        this.listeners.message.forEach((callback) => callback(event.data));
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.listeners.error.forEach((callback) => callback(error));
      };
    } catch (error) {
      console.error("Failed to create WebSocket:", error);
      this.attemptReconnect();
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(
        `Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`
      );
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error("Max reconnection attempts reached");
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      // Support both text and binary (ArrayBuffer) messages
      if (message instanceof ArrayBuffer) {
        this.ws.send(message);
      } else {
        this.ws.send(message);
      }
      return true;
    } else {
      console.warn("WebSocket is not connected. Message not sent:", message);
      return false;
    }
  }

  close() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  on(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback);
    }
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(
        (cb) => cb !== callback
      );
    }
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

export default WebSocketClient;

