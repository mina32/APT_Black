package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class NearbyActivity extends AppCompatActivity implements View.OnClickListener
{
    private Intent userDataIntent;
    Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nearby);
        userDataIntent = getIntent();

        findViewById(R.id.button_view_streams).setOnClickListener(this);
    }

    @Override
    public void  onStart() {
        super.onStart();
        //TODO: Get Actual Location -- stubbed vavlues for now
        AsyncHttp nav = new AsyncHttp(context, findViewById(R.id.nearby_streams_grid), userDataIntent);
        nav.getNearbyStreams(30.1378, -97.5512);
    }

    @Override
    public void onClick(View view) {
        switch(view.getId()){
            case R.id.button_view_streams:
                userDataIntent.setClass(context, AllStreamActivity.class);
                startActivity(userDataIntent);
                break;
            case R.id.button_more2:
                //TODO: same layout, different images
                break;

        }

    }
}
