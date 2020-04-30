import React from 'react';
import { ActivityIndicator, Button, View, Platform } from 'react-native';
import Svg, { Circle, Rect, G, Line } from 'react-native-svg';
import '@tensorflow/tfjs-react-native';

import * as Permissions from 'expo-permissions';
import { Camera } from 'expo-camera';
import { ExpoWebGLRenderingContext } from 'expo-gl';

import * as tf from '@tensorflow/tfjs';
import * as posenet from '@tensorflow-models/posenet';
import { cameraWithTensors } from '@tensorflow/tfjs-react-native';

import { styles } from './styles';
import { pose_ready } from './pose-ready';

interface ScreenProps {
  returnToMain: () => void;
}

interface ScreenState {
  hasCameraPermission?: boolean;
  cameraType: any;
  isLoading: boolean;
  posenetModel?: posenet.PoseNet;
  pose?: posenet.Pose;
}

const inputTensorWidth = 152;
const inputTensorHeight = 200;

const AUTORENDER = true;

const TensorCamera = cameraWithTensors(Camera);

export class RealtimeDemo extends React.Component<ScreenProps, ScreenState> {
  rafID?: number;

  constructor(props: ScreenProps) {
    super(props);
    this.state = {
      isLoading: true,
      cameraType: Camera.Constants.Type.front
    };
    this.handleImageTensorReady = this.handleImageTensorReady.bind(this);
  }
  // {
  //   architecture: 'MobileNetV1',
  //   outputStride: 16,
  //   inputResolution: { width: inputTensorWidth, height: inputTensorHeight },
  //   multiplier: 0.75,
  //   quantBytes: 2
  // }
  async loadPosenetModel() {
    const model = await posenet.load();
    return model;
  }

  async handleImageTensorReady(
    images: IterableIterator<tf.Tensor3D>,
    updatePreview: () => void,
    gl: ExpoWebGLRenderingContext
  ) {
    const loop = async () => {
      if (!AUTORENDER) {
        updatePreview();
      }

      if (this.state.posenetModel != null) {
        const imageTensor = images.next().value;
        const flipHorizontal = Platform.OS === 'ios' ? false : true;
        const pose = await this.state.posenetModel.estimateSinglePose(
          imageTensor,
          { flipHorizontal }
        );
        this.setState({ pose });
        pose_ready(pose)
        tf.dispose([imageTensor]);
      }

      if (!AUTORENDER) {
        gl.endFrameEXP();
      }
      this.rafID = requestAnimationFrame(loop);
    };

    loop();
  }

  componentWillUnmount() {
    if (this.rafID) {
      cancelAnimationFrame(this.rafID);
    }
  }

  async componentDidMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    console.log(status);
    await tf.ready();
    console.log('TF.READY wooorks');
    const posenetModel = await this.loadPosenetModel();

    this.setState({
      hasCameraPermission: status === 'granted',
      isLoading: false,
      posenetModel
    });
  }

  renderPose() {
    const MIN_KEYPOINT_SCORE = 0.2;
    const { pose } = this.state;
    if (pose != null) {
      const keypoints = pose.keypoints
        .filter(k => k.score > MIN_KEYPOINT_SCORE)
        .map((k, i) => {
          return (
            <Circle
              key={`skeletonkp_${i}`}
              cx={k.position.x}
              cy={k.position.y}
              r='2'
              strokeWidth='0'
              fill='blue'
            />
          );
        });

      const adjacentKeypoints = posenet.getAdjacentKeyPoints(
        pose.keypoints,
        MIN_KEYPOINT_SCORE
      );

      const skeleton = adjacentKeypoints.map(([from, to], i) => {
        return (
          <Line
            key={`skeletonls_${i}`}
            x1={from.position.x}
            y1={from.position.y}
            x2={to.position.x}
            y2={to.position.y}
            stroke='magenta'
            strokeWidth='1'
          />
        );
      });

      return (
        <Svg
          height='100%'
          width='100%'
          viewBox={`0 0 ${inputTensorWidth} ${inputTensorHeight}`}>
          {skeleton}
          {keypoints}
        </Svg>
      );
    } else {
      return null;
    }
  }

  flipCam(){
    this.setState({
      cameraType: this.state.cameraType === Camera.Constants.Type.back ? Camera.Constants.Type.front : Camera.Constants.Type.back
    })
  }

  render() {
    const { isLoading } = this.state;

    // TODO File issue to be able get this from expo.
    // Caller will still need to account for orientation/phone rotation changes
    let textureDims: { width: number; height: number };
    if (Platform.OS === 'ios') {
      textureDims = {
        height: 1920,
        width: 1080
      };
    } else {
      textureDims = {
        height: 1200,
        width: 1600
      };
    }

    const camView = (
      <View style={styles.cameraContainer}>
        <View style={styles.sectionContainer}>
          <Button onPress={this.props.returnToMain} title='Back' />
          <Button onPress={ () => this.flipCam()} title='Flip' />
        </View>

        <TensorCamera
          // Standard Camera props
          style={styles.camera}
          type={this.state.cameraType}
          zoom={0}
          // tensor related props
          cameraTextureHeight={textureDims.height}
          cameraTextureWidth={textureDims.width}
          resizeHeight={inputTensorHeight}
          resizeWidth={inputTensorWidth}
          resizeDepth={3}
          onReady={this.handleImageTensorReady}
          autorender={AUTORENDER}
        />
        <View style={styles.modelResults}>{this.renderPose()}</View>
      </View>
    );

    return (
      <View style={styles.realTimeContainer}>
        {isLoading ? (
          <View style={[styles.loadingIndicator]}>
            <ActivityIndicator size='large' color='#FF0266' />
          </View>
        ) : (
          camView
        )}

      </View>
    );
  }
}
