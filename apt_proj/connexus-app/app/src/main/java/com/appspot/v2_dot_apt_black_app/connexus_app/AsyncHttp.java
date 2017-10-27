package com.appspot.v2_dot_apt_black_app.connexus_app;

/**
 * Created by brice on 10/22/17.
 */


import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.GridLayout;
import android.widget.Toast;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import cz.msebera.android.httpclient.Header;


public class AsyncHttp  extends AppCompatActivity
{
    private static final String BASE_URL = "http://v3-dot-apt-black-app.appspot.com";

    private Context context;
    private View viewToModify;
    private Intent userDataIntent;
    private AsyncHttpClient client;
    private boolean userIsSignedIn;

    public AsyncHttp(Context context, View view, Intent userDataIntent)
    {
        this.context = context;
        this.viewToModify = view;
        this.userDataIntent = userDataIntent;
        this.userIsSignedIn = (userDataIntent.getStringExtra("userId") != null);
        this.client = new AsyncHttpClient();
    }

    private void get(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.get(getAbsoluteUrl(url), params, responseHandler);
    }

    private void post(String url, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.post(getAbsoluteUrl(url), params, responseHandler);
    }

    private String getAbsoluteUrl(String relativeUrl) {
        String REQ = "userEmail";
        String uriRequested = BASE_URL + relativeUrl;

        if (userIsSignedIn) {
            String userEmail = userDataIntent.getStringExtra(REQ);
            if (!uriRequested.contains("?")) {
                uriRequested += "?" + REQ + "=" + userEmail;
            } else {
                uriRequested += "&" + REQ + "=" + userEmail;
            }
        }

//        Toast.makeText(context, uriRequested, Toast.LENGTH_SHORT).show();
        return uriRequested;
    }

    private void update16BoxGridLayout(final JsonArray streams)
    {
        GridLayout gridLayout = (GridLayout) viewToModify;
        gridLayout.removeAllViews();

        int rows = 4;
        int columns = 4;
        gridLayout.setColumnCount(columns);
        gridLayout.setRowCount(rows);

        int i = 0;
        for(int c = 0; c < columns; c++)
        {
            for(int r = 0; r < rows; r++)
            {
                JsonObject jObj = null;
                if(streams != null && i < streams.size())
                {
                    jObj = (JsonObject) streams.get(i);
                }

                ConnexusButton oImageButton = new ConnexusButton(context, jObj, userDataIntent);
                GridLayout.Spec rowSpan = GridLayout.spec(GridLayout.UNDEFINED, 1);
                GridLayout.Spec colspan = GridLayout.spec(GridLayout.UNDEFINED, 1);
                GridLayout.LayoutParams gridParam = new GridLayout.LayoutParams(rowSpan, colspan);
                gridLayout.addView(oImageButton, gridParam);
                i++;
            }
        }
    }

    private void update16BoxGridView(final JsonArray images)
    {
        GridLayout gridLayout = (GridLayout) viewToModify;
        gridLayout.removeAllViews();

        int rows = 4;
        int columns = 4;
        gridLayout.setColumnCount(columns);
        gridLayout.setRowCount(rows);

        int i = 0;
        for(int c = 0; c < columns; c++)
        {
            for(int r = 0; r < rows; r++)
            {
                JsonObject jObj = null;
                if(images != null && i < images.size())
                {
                    jObj = (JsonObject) images.get(i);
                }

                ConnexusImageView oImageView = new ConnexusImageView(context, jObj, userDataIntent);
                GridLayout.Spec rowSpan = GridLayout.spec(GridLayout.UNDEFINED, 1);
                GridLayout.Spec colspan = GridLayout.spec(GridLayout.UNDEFINED, 1);
                GridLayout.LayoutParams gridParam = new GridLayout.LayoutParams(rowSpan, colspan);
                gridLayout.addView(oImageView, gridParam);
                i++;
            }
        }
    }

    // [ START Get Most recently updated streams]
    private  void recentlyUpdatedStreamsHandler(byte[] response)
    {
        try
        {
            String s = new String(response);
            JsonParser parser = new JsonParser();
            JsonObject json = parser.parse(s).getAsJsonObject();
            JsonArray streams = json.get("all_streams").getAsJsonArray();
            update16BoxGridLayout(streams);
        }
        catch(Exception e)
        {
            update16BoxGridLayout(null);
        }
    }

    public void getMostRecentlyUpdatedStreams()
    {
        AsyncHttpResponseHandler respHandler = new  AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response)
            {
                recentlyUpdatedStreamsHandler(response);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
                Toast.makeText(context, "Server connection failed! " + statusCode, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onRetry(int retryNo)
            {
                Toast.makeText(context, "Retry " + retryNo, Toast.LENGTH_SHORT).show();
                if(retryNo == 2)
                    return;
            }
        };

        get("/androidMostViewed",null, respHandler);
    }
    // [END Get Most recently updated streams]

    // [ START My subscribed streams button]
    private  void subscribedStreamsHandler(byte[] response)
    {
        try
        {
            String s = new String(response);
            JsonParser parser = new JsonParser();
            JsonObject json = parser.parse(s).getAsJsonObject();
            JsonArray streams = json.get("subscribed_streams").getAsJsonArray();
            update16BoxGridLayout(streams);
        }
        catch(Exception e)
        {
            update16BoxGridLayout(null);
        }
    }

    public void getMostSubscribedStreams()
    {
        AsyncHttpResponseHandler respHandler = new  AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response)
            {
                subscribedStreamsHandler(response);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e)
            {
                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
                Toast.makeText(context, "Server connection failed! " + statusCode, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onRetry(int retryNo)
            {
                Toast.makeText(context, "Retry " + retryNo, Toast.LENGTH_SHORT).show();
                if(retryNo == 2)
                    return;
            }
        };

        get("/androidSubscribedStreams",null, respHandler);
    }
    // [END My subscribed streams button]

    // [ START showStreamPicture]
    private  void showStreamPicturesHandler(byte[] response)
    {
        try
        {
            String s = new String(response);
            JsonParser parser = new JsonParser();
            JsonObject json = parser.parse(s).getAsJsonObject();
            JsonArray images = json.get("media_items").getAsJsonArray();
            update16BoxGridView(images);
        }
        catch(Exception e)
        {
            update16BoxGridView(null);
        }
    }

    public void showStreamPicture()
    {
        AsyncHttpResponseHandler respHandler = new  AsyncHttpResponseHandler()
        {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response)
            {
                showStreamPicturesHandler(response);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e)
            {
                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
                Toast.makeText(context, "Server connection failed! " + statusCode, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onRetry(int retryNo)
            {
                Toast.makeText(context, "Retry " + retryNo, Toast.LENGTH_SHORT).show();
                if(retryNo == 2)
                {
                    return;
                }
            }
        };

        get("/androidViewImages" + "?key_url=" + userDataIntent.getStringExtra("key_url"), null, respHandler);
    }
    // [END showStreamPicture]

    // TODO: Implement Post image: Next on Brice, Anyone feel free to take though

    
    // [ START getNearby ]
    private  void getNearbyHandler(byte[] response)
    {
        try
        {
            String s = new String(response);
            JsonParser parser = new JsonParser();
            JsonObject json = parser.parse(s).getAsJsonObject();
            JsonArray streams = json.get("streams_by_distance").getAsJsonArray();
            update16BoxGridLayout(streams);
        }
        catch(Exception e)
        {
            update16BoxGridLayout(null);
        }
    }

    public void getNearbyStreams(String lat, String lon)
    {
        Log.i("=======>", "Getting Nearby!!!");
        AsyncHttpResponseHandler respHandler = new  AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response)
            {
                getNearbyHandler(response);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e)
            {
                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
                Toast.makeText(context, "Server connection failed! " + statusCode, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onRetry(int retryNo)
            {
                Toast.makeText(context, "Retry " + retryNo, Toast.LENGTH_SHORT).show();
                if(retryNo == 2)
                    return;
            }
        };
        RequestParams req = new RequestParams();
        req.put("lat", lat);
        req.put("lon", lon);
        get("/androidNearbyResults", req, respHandler);
    }
    // [END getNearby ]


    // [ START Search streams ]
    private  void searchStreamsHandler(byte[] response)
    {
        try
        {
            String s = new String(response);
            JsonParser parser = new JsonParser();
            JsonObject json = parser.parse(s).getAsJsonObject();
            JsonArray streams = json.get("search_streams").getAsJsonArray();
            update16BoxGridLayout(streams);
        }
        catch(Exception e)
        {
            update16BoxGridLayout(null);
        }
    }

    public void getSearchStreams(String query)
    {
        AsyncHttpResponseHandler respHandler = new  AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response)
            {
                searchStreamsHandler(response);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e)
            {
                // called when response HTTP status is "4XX" (eg. 401, 403, 404)
                Toast.makeText(context, "Server connection failed! " + statusCode, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onRetry(int retryNo)
            {
                Toast.makeText(context, "Retry " + retryNo, Toast.LENGTH_SHORT).show();
                if(retryNo == 2)
                    return;
            }
        };
        RequestParams req = new RequestParams();
        req.put("query", query);
        get("/androidSearchResults", req, respHandler);
    }
    // [END Search streams ]
    // TODO: Use getMostSubscribedStreams to solve the right above two TODOS.
}