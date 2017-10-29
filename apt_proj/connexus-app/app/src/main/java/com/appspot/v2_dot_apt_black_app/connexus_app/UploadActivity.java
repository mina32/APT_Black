package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.IdRes;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.File;
import java.util.HashMap;

public class UploadActivity extends AppCompatActivity implements View.OnClickListener {
    Context context = this;

    private Bitmap myBitmap = null;
    private Intent userDataIntent;
    private static final String TAG = "UploadActivity";

    private HashMap response = new HashMap();
    private EditText comment;

    @Override
    public View findViewById(@IdRes int id) {
        return super.findViewById(id);
    }

    public static final int PICK_IMAGE = 1;
    public static final int UPLOAD_IMAGE = 2;

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        //TODO: Is this the right idea?
        switch(requestCode) {
            case(PICK_IMAGE):
                Uri pickedImage = data.getData();
                try {
                    myBitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), pickedImage);
                    response.put("imageFile", myBitmap);
                } catch (Exception e) {
                    Log.i("ERR:", e.toString());
                }
                break;
            case(UPLOAD_IMAGE):
                // send POST to /post_media/<streamID>
                if (resultCode == RESULT_OK) {
                    // get the captured image
                    Bundle b = data.getExtras();
                    File f = (File) b.getSerializable("pictureFile");
                    Log.v(TAG,"captured file: " + f.getAbsolutePath());
                    myBitmap = BitmapFactory.decodeFile(f.getAbsolutePath());
                    response.put("imageFile", myBitmap);
                }
                break;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_upload);
        //response.put(uploadImage);
        comment = (EditText)findViewById(R.id.text_comment);

        userDataIntent = getIntent();
        findViewById(R.id.button_choose).setOnClickListener(this);
        findViewById(R.id.button_camera).setOnClickListener(this);
        findViewById(R.id.button_upload).setOnClickListener(this);


    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.button_choose:
                Intent intent = new Intent();
                intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);
                startActivityForResult(Intent.createChooser(intent, "Select Picture"), PICK_IMAGE);
                break;
            case R.id.button_camera:
                Intent cameraIntent = new Intent(UploadActivity.this, CameraActivity.class);
                startActivityForResult(cameraIntent, UPLOAD_IMAGE);
                break;
            case R.id.button_upload:
                if (myBitmap == null) {
                    Toast.makeText(UploadActivity.this, "Please choose a picture.", Toast.LENGTH_SHORT).show();
                }
                response.put("uploadComment",comment.getText().toString());
                // TODO: send POST to /post_media/<streamID>
                break;
        }
    }
}
