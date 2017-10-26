package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;


public class CameraActivity extends AppCompatActivity {
    Context context = this;

    private Intent intent;
    private File pictureFile = null;

    private ImageView imageHolder;

    private ImageButton takepicButton;
    private Button usepicButton;
    private Button streamButton;

    private Bitmap bitmap;
    private static final String TAG = "CameraActivity";
    private final int requestCode = 20;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        imageHolder = (ImageView)findViewById(R.id.preview);
        takepicButton = (ImageButton)findViewById(R.id.button_takepicture);
        takepicButton.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent photoCaptureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(photoCaptureIntent, requestCode);
            }
        });

        usepicButton = (Button)findViewById(R.id.button_usepicture);
        usepicButton.setEnabled(false);
        usepicButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(bitmap != null) {
                    Toast.makeText(CameraActivity.this, "Saving Image...", Toast.LENGTH_SHORT).show();
                    FileOutputStream fos = null;
                    try{
                        pictureFile = createImageFile();
                        fos = new FileOutputStream(pictureFile);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    bitmap.compress(Bitmap.CompressFormat.JPEG,100, fos);
                    Log.v(TAG,"file written to " + pictureFile.getAbsolutePath());
                    intent = new Intent();
                    intent.putExtra("pictureFile", pictureFile);
                    setResult(Activity.RESULT_OK, intent);
                    finish();
                }
            }
        });

        streamButton = (Button)findViewById(R.id.button_streams);
        streamButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent streamIntent = new Intent();
                streamIntent.setClass(CameraActivity.this, AllStreamActivity.class);
                startActivity(streamIntent);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(this.requestCode == requestCode && resultCode == RESULT_OK){
            bitmap = (Bitmap)data.getExtras().get("data");
            imageHolder.setImageBitmap(bitmap);
            usepicButton.setEnabled(true);

        }
    }

    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );
        return image;
    }

}