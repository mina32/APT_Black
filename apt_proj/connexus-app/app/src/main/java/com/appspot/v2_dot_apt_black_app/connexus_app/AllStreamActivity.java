package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

import com.google.android.gms.common.api.GoogleApiClient;

public class AllStreamActivity extends AppCompatActivity implements View.OnClickListener{

    private Button mSearchButton;
    private ImageButton mNearby;
    private Button mSubscribe;

    Context context = this;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_allstream);

        findViewById(R.id.search_button).setOnClickListener(this);
        findViewById(R.id.button_nearby).setOnClickListener(this);
        findViewById(R.id.subscribed_button).setOnClickListener(this);



    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.search_button:
                Intent searchIntent = new Intent(context, SearchActivity.class);
                startActivity(searchIntent);
                break;
            case R.id.button_nearby:
                Intent nearIntent = new Intent(context, NearbyActivity.class);
                startActivity(nearIntent);
                break;
            case R.id.subscribed_button:
               //TODO:same layout but different images
                break;
        }
    }
}
