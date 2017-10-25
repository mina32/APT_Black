package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class NearbyActivity extends AppCompatActivity implements View.OnClickListener
{
    Intent intent;
    Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nearby);
        intent = getIntent();

        findViewById(R.id.button_view_streams).setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch(view.getId()){
            case R.id.button_view_streams:
                intent.setClass(context, AllStreamActivity.class);
                startActivity(intent);
                break;
            case R.id.button_more2:
                //TODO: same layout, different images
                break;

        }

    }
}
