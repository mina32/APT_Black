package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;

public class NearbyActivity extends AppCompatActivity implements View.OnClickListener,
        GoogleApiClient.ConnectionCallbacks
{
    public static final int MY_PERMISSIONS_REQUEST_LOCATION = 99;
    private Intent userDataIntent;
    Context context = this;
    GoogleApiClient mGoogleApiClient;
    Location mLastLocation;
    String mLatitudeText;
    String mLongitudeText;
    AsyncHttp nav;
    private static final String TAG = "NearbyActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nearby);
        userDataIntent = getIntent();
        if (mGoogleApiClient == null) {
            mGoogleApiClient = new GoogleApiClient.Builder(this)
                    .addConnectionCallbacks(this)
                    //.addOnConnectionFailedListener(this)
                    .addApi(LocationServices.API)
                    .build();
        }
        nav = new AsyncHttp(context, findViewById(R.id.nearby_streams_grid), userDataIntent);
        findViewById(R.id.button_view_streams).setOnClickListener(this);
        findViewById(R.id.button_more2).setOnClickListener(this);
    }
    @Override
    public void onConnected(Bundle connectionHint) {
        if (ContextCompat.checkSelfPermission(context, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.v(TAG,"Permission ERR");
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    MY_PERMISSIONS_REQUEST_LOCATION);
            //return;
        }
        // This is the first time calling the getLastLocation. That might not be
        // enough time for the first location to come in. So put in a loop.
        int count = 0;
        while (mLastLocation == null && count < 500) {
            mLastLocation = LocationServices.FusedLocationApi.getLastLocation(
                    mGoogleApiClient);
            count++;
        }
         if (mLastLocation != null) {
            mLatitudeText = String.valueOf(mLastLocation.getLatitude());
            mLongitudeText = String.valueOf(mLastLocation.getLongitude());
        } else if (count == 500) {
             Toast.makeText(NearbyActivity.this, "Location not available, using default location.", Toast.LENGTH_SHORT).show();
             mLatitudeText = "30.2890";
             mLongitudeText = "-97.7355";
         }
        Log.v(TAG,"Latitude:: " + mLatitudeText);
        nav.getNearbyStreams(mLatitudeText, mLongitudeText);
    }

    @Override
    public void onConnectionSuspended(int code) {
        return;
    }

    @Override
    public void  onStart() {
        mGoogleApiClient.connect();
        super.onStart();
    }

    protected void onStop() {
        mGoogleApiClient.disconnect();
        super.onStop();
    }


    @Override
    public void onClick(View view) {
        switch(view.getId()){
            case R.id.button_view_streams:
                userDataIntent.setClass(context, AllStreamActivity.class);
                startActivity(userDataIntent);
                break;
            case R.id.button_more2:
                nav.showMorePictures();
                break;

        }

    }

}
