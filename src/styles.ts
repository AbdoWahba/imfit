import { StyleSheet } from 'react-native';
import { Dimensions } from "react-native";

export const styles = StyleSheet.create({
  appContainer:{
    flex: 1,
  },
  realTimeContainer:{
    paddingTop: 32
  },
  loadingIndicator: {
    position: 'absolute',
    top: 20,
    right: 20,
    zIndex: 200
  },
  sectionContainer: {
    position: 'absolute',
    bottom: 15,
    right: 15,
    zIndex: 40,
    flexDirection: 'row',
  },
  cameraContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '100%',
    backgroundColor: '#fff',
  },
  camera: {
    position: 'absolute',
    left: 0,
    top: 0,
    right: 0,
    bottom: 0,
    width: Dimensions.get('window').width,
    height: ((Dimensions.get('window').width * 4)/3),
    zIndex: 1,
    borderWidth: 1,
    borderColor: 'black',
    borderRadius: 0
  },
  modelResults: {
    position: 'absolute',
    left: 0,
    top: 0,
    right: 0,
    bottom: 0,
    width: Dimensions.get('window').width,
    height: ((Dimensions.get('window').width * 4)/3),
    zIndex: 20,
    borderWidth: 1,
    borderColor: 'black',
    borderRadius: 0
  }
});
