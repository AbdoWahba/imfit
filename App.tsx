import React from 'react';
import { View } from 'react-native';
import { RealtimeDemo as Realtime } from './src/RealtimeDemo';
import { styles } from './src/styles';
export default function App() {
  return (
    <View style={styles.appContainer}>
      <Realtime returnToMain={(): void => console.log('hello')} />
    </View>
  );
}
