package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.SearchView;

import static com.appspot.v2_dot_apt_black_app.connexus_app.R.id.search;

public class SearchActivity extends AppCompatActivity implements View.OnClickListener
{
    private Intent userDataIntent;
    Context context = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
        userDataIntent = getIntent();
        findViewById(R.id.search_button).setOnClickListener(this);
    }
    @Override
    public void  onStart()
    {
        super.onStart();
        String searchText = getIntent().getStringExtra("QUERY");
        AsyncHttp nav = new AsyncHttp(context, findViewById(R.id.search_streams_grid), userDataIntent);
        nav.getSearchStreams(searchText);
    }

    @Override
    public void onClick(View view)
    {
        switch (view.getId()) {
            case R.id.search_button:
                SearchView searchWidget = (SearchView) findViewById(search);
                String searchText = searchWidget.getQuery().toString();
                AsyncHttp nav = new AsyncHttp(context, findViewById(R.id.search_streams_grid), userDataIntent);
                nav.getSearchStreams(searchText);
                break;
        }
    }

}
