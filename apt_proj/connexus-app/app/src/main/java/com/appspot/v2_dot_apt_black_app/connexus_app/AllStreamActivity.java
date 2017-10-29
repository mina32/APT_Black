package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.SearchView;

import static com.appspot.v2_dot_apt_black_app.connexus_app.R.id.search_all;


public class AllStreamActivity extends AppCompatActivity implements View.OnClickListener
{
    private Intent userDataIntent;
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
        updateVisibility();
    }

    @Override
    public void onResume()
    {
        super.onResume();
        updateVisibility();
    }

    @Override
    public void  onStart()
    {
        super.onStart();
        updateVisibility();
        AsyncHttp navigator = new AsyncHttp(context, findViewById(R.id.all_streams_grid), userDataIntent);
        navigator.getMostRecentlyUpdatedStreams();
    }

    @Override
    public void onClick(View view)
    {
        switch (view.getId()) {
            case R.id.search_button:
                SearchView searchWidget = (SearchView) findViewById(search_all);
                String searchText = searchWidget.getQuery().toString();
                userDataIntent.setClass(context, SearchActivity.class);
                userDataIntent.putExtra("QUERY", searchText);
                startActivity(userDataIntent);
                break;
            case R.id.button_nearby:
                userDataIntent.setClass(context, NearbyActivity.class);
                startActivity(userDataIntent);
                break;
            case R.id.subscribed_button:
                AsyncHttp navigator = new AsyncHttp(context, findViewById(R.id.all_streams_grid), userDataIntent);
                navigator.getMostSubscribedStreams();
                break;
        }
    }
}
