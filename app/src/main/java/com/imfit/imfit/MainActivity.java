package com.imfit.imfit;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceView;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCamera2View;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;
import org.opencv.video.BackgroundSubtractorMOG2;
import org.opencv.video.Video;

public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    private static String TAG = "MainActivity";

    JavaCamera2View javaCameraView;
    private Mat mRGBA, mRGBAT;

    BackgroundSubtractorMOG2 fgbg;
    float x[] = {};
    float y[] = {};
    float xall[] = {};
    float xall2[] = {};
    float yall[] = {};
    int counter = 0;
    float testnet[] = {};
    int t = 0;

    static {
    }

    private BaseLoaderCallback loaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {

            switch (status){
                case BaseLoaderCallback.SUCCESS: {
                    Log.d(TAG, "Loader Callback SUCCESS");
                    javaCameraView.enableView();

                    fgbg = Video.createBackgroundSubtractorMOG2();
                }
                    break;

                default: {
                    Log.d(TAG, "Loader Callback default");
                    super.onManagerConnected(status);
                }
                    break;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 100);
        }

        this.javaCameraView = (JavaCamera2View) findViewById(R.id.camera_view_el);
        this.javaCameraView.setCameraIndex(1);

        this.javaCameraView.setVisibility(SurfaceView.VISIBLE);
        this.javaCameraView.setCvCameraViewListener(this);

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode){
            case 100: {
                if(grantResults.length>0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    loaderCallback.onManagerConnected(BaseLoaderCallback.SUCCESS);
                }
            }
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    @Override
    protected void onPause() {
        super.onPause();

        if(this.javaCameraView != null) this.javaCameraView.disableView();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if(this.javaCameraView != null) this.javaCameraView.disableView();
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (OpenCVLoader.initDebug()) {
            Log.d(TAG, "OpenCV Configured Successfully");
            loaderCallback.onManagerConnected(BaseLoaderCallback.SUCCESS);
        } else {
            Log.d(TAG, "OpenCV NOT Configured Successfully");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION, this, this.loaderCallback);
        }

    }

    @Override
    public void onCameraViewStarted(int width, int height) {
        mRGBA = new Mat(width, height, CvType.CV_8UC4);
    }

    @Override
    public void onCameraViewStopped() {
        mRGBA.release();
    }

    public Mat pushups(Mat frame){
        Mat fgmask = frame;
        fgbg.apply(frame, fgmask);

        // Here

        return fgmask;
    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {

        System.gc();

        this.mRGBA = inputFrame.rgba();
        mRGBAT = mRGBA.t();
        Core.flip(mRGBA.t(), mRGBAT, -1);
        Imgproc.resize(mRGBAT, mRGBAT, mRGBA.size());

        Mat xx = pushups(mRGBAT);

        return xx;
    }

    @Override
    public void onPointerCaptureChanged(boolean hasCapture) {

    }
}
