import threading
import json
import time
import logging
import websocket

logger = logging.getLogger(__name__)


class SpeakerClient:
    def __init__(self):
        self._lock = threading.Lock()
        self._ws = None
        self._heartbeat_timer = None
        self._running = False
        self._speaker_ip = ''
        self._heartbeat_interval = 10
        self._reconnect_delay = 3
        self._max_reconnect_delay = 60

    def configure(self, speaker_ip, heartbeat_interval=10):
        old_ip = self._speaker_ip
        self._speaker_ip = speaker_ip
        self._heartbeat_interval = max(1, int(heartbeat_interval))
        if old_ip != speaker_ip and self._running:
            self._disconnect()
            if speaker_ip:
                self._schedule_connect(1)

    def start(self):
        if not self._running:
            self._running = True
            if self._speaker_ip:
                self._schedule_connect(0)

    def stop(self):
        self._running = False
        self._disconnect()

    def _get_url(self):
        return f'ws://{self._speaker_ip}:18888/ws/status'

    def _schedule_connect(self, delay):
        t = threading.Timer(delay, self._connect_loop)
        t.daemon = True
        t.start()

    def _connect_loop(self):
        if not self._running or not self._speaker_ip:
            return
        url = self._get_url()
        logger.info(f'[SpeakerClient] Connecting to {url}')
        try:
            ws = websocket.WebSocketApp(
                url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
            )
            with self._lock:
                self._ws = ws
            self._reconnect_delay = 3
            ws.run_forever()
        except Exception as e:
            logger.error(f'[SpeakerClient] Connection error: {e}')
            self._handle_reconnect()

    def _on_open(self, ws):
        logger.info('[SpeakerClient] Connected')
        self._reconnect_delay = 3
        self._start_heartbeat()

    def _on_message(self, ws, message):
        pass

    def _on_error(self, ws, error):
        logger.warning(f'[SpeakerClient] Error: {error}')

    def _on_close(self, ws, close_status_code, close_msg):
        logger.info('[SpeakerClient] Connection closed')
        self._stop_heartbeat()
        self._handle_reconnect()

    def _handle_reconnect(self):
        if self._running and self._speaker_ip:
            logger.info(f'[SpeakerClient] Reconnecting in {self._reconnect_delay}s')
            self._schedule_connect(self._reconnect_delay)
            self._reconnect_delay = min(self._reconnect_delay * 2, self._max_reconnect_delay)

    def _start_heartbeat(self):
        self._stop_heartbeat()
        self._send_ping()

    def _send_ping(self):
        if not self._running:
            return
        with self._lock:
            ws = self._ws
        if ws:
            try:
                ws.send(json.dumps({'action': 'ping'}))
            except Exception as e:
                logger.warning(f'[SpeakerClient] Heartbeat error: {e}')
        self._heartbeat_timer = threading.Timer(self._heartbeat_interval, self._send_ping)
        self._heartbeat_timer.daemon = True
        self._heartbeat_timer.start()

    def _stop_heartbeat(self):
        if self._heartbeat_timer:
            self._heartbeat_timer.cancel()
            self._heartbeat_timer = None

    def _disconnect(self):
        self._stop_heartbeat()
        with self._lock:
            ws = self._ws
            self._ws = None
        if ws:
            try:
                ws.close()
            except Exception:
                pass

    def send_text(self, text):
        """发送语音播报文本，返回是否发送成功"""
        with self._lock:
            ws = self._ws
        if not ws:
            logger.warning('[SpeakerClient] Not connected, message dropped')
            return False
        payload = {
            'action': 'message',
            'data': {
                'what': 65536,
                'arg1': 0,
                'arg2': 0,
                'obj': text
            }
        }
        try:
            ws.send(json.dumps(payload, ensure_ascii=False))
            logger.info(f'[SpeakerClient] Sent: {text[:50]}...' if len(text) > 50 else f'[SpeakerClient] Sent: {text}')
            return True
        except Exception as e:
            logger.error(f'[SpeakerClient] Send error: {e}')
            return False


# 全局单例
speaker_client = SpeakerClient()
