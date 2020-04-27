import React from 'react';
import { View } from 'react-native';
import { RealtimeDemo as Realtime } from './src/realtime_demo';
export default function App() {
  return (
    <View>
      <Realtime returnToMain={(): void => console.log('hello')} />
    </View>
  );
}
