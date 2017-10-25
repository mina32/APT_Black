package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.IdRes;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

import java.util.HashMap;

public class UploadActivity extends AppCompatActivity implements View.OnClickListener {
    Context context = this;
    private Intent userDataIntent;
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
                response.put("uploadImage", data);
                break;
            case(UPLOAD_IMAGE):
                // send POST to /post_media/<streamID>
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
                Intent nearIntent = new Intent(context, CameraActivity.class);
                startActivity(nearIntent);
                break;
            case R.id.button_upload:
                response.put("uploadComment",comment.getText().toString());
                // TODO: send POST to /post_media/<streamID>
                break;
        }
    }
}
