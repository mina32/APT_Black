package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class SingleStreamActivity extends AppCompatActivity implements View.OnClickListener {
    private Intent intent;
    AsyncHttp navigator;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_single_stream);

        intent = getIntent();

        findViewById(R.id.button_more).setOnClickListener(this);
        findViewById(R.id.button_upload).setOnClickListener(this);
        findViewById(R.id.button_streams).setOnClickListener(this);

        Toast.makeText(this, "Single View create", Toast.LENGTH_SHORT).show();
        TextView streamName = (TextView) findViewById(R.id.stream_name);
        streamName.setText("Stream name: " + intent.getStringExtra("stream_name"));
        navigator = new AsyncHttp(this, findViewById(R.id.view_single_grid), intent);

        navigator.showStreamPicture();
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.button_more:
                navigator.showMorePictures();
                break;
            case R.id.button_upload:
                intent.setClass(this, UploadActivity.class);
                startActivity(intent);
                break;
            case R.id.button_streams:
                intent.setClass(this, AllStreamActivity.class);
                startActivity(intent);
                break;
        }
    }
}
