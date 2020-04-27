import React from 'react';
import { View } from 'react-native';
import { RealtimeDemo as Realtime } from './src/RealtimeDemo';
export default function App() {
  return (
    <View>
      <Realtime returnToMain={(): void => console.log('hello')} />
    </View>
  );
}
