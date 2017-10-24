package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.auth.api.signin.GoogleSignInAccount;

public class AllStreamActivity extends AppCompatActivity implements View.OnClickListener
{
    private Intent userDataIntent;
    private boolean userIsAuthed;
    private GoogleSignInAccount acct = null;

    private Button mSearchButton;
    private ImageButton mNearby;
    private Button mSubscribe;

    Context context = this;

    private void updateVisibility()
    {
        if(userDataIntent.getStringExtra("userId") == null)
        {
            findViewById(R.id.subscribed_button).setVisibility(View.INVISIBLE);
        }
        else
        {
            findViewById(R.id.subscribed_button).setVisibility(View.VISIBLE);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_allstream);

        userDataIntent = getIntent();
        findViewById(R.id.search_button).setOnClickListener(this);
        findViewById(R.id.button_nearby).setOnClickListener(this);
        findViewById(R.id.subscribed_button).setOnClickListener(this);

        Toast.makeText(context, "Acct create", Toast.LENGTH_SHORT).show();
        updateVisibility();
    }

    @Override
    public void onResume()
    {
        Toast.makeText(context, "Acct resume", Toast.LENGTH_SHORT).show();
        super.onResume();
        updateVisibility();
    }

    @Override
    public void  onStart()
    {
        super.onStart();
        updateVisibility();

        Toast.makeText(context, "AllStream Start", Toast.LENGTH_SHORT).show();
        AsyncHttp navigator = new AsyncHttp(context, findViewById(R.id.all_streams_grid), userDataIntent);
        navigator.getMostRecentlyUpdatedStreams();
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
                AsyncHttp navigator = new AsyncHttp(context, findViewById(R.id.all_streams_grid), userDataIntent);
                navigator.getMostSubscribedStreams();
                break;
        }
    }
}
