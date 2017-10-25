package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.OptionalPendingResult;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;

import java.io.Serializable;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

/**
 * Activity to demonstrate basic retrieval of the Google user's ID, email address, and basic
 * profile.
 */
public class SignInActivity extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener,
        View.OnClickListener
{
    Context context = this;
    private static final String TAG = "SignInActivity";
    private static final int RC_SIGN_IN = 9001;
    private static final int RC_SIGN_OUT = 9002;

    private GoogleSignInAccount acct = null;
    private GoogleApiClient mGoogleApiClient;

    private static final String OATUH2_WEB_CLIENT = "878862959391-mm4e2g0acdctndbfodennioaeqffa8ig.apps.googleusercontent.com";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signin);

        // Button listeners
        findViewById(R.id.button_sign_in).setOnClickListener(this);
        findViewById(R.id.button_sign_out).setOnClickListener(this);
        findViewById(R.id.button_view_streams).setOnClickListener(this);

        // [START configure_signin]
        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                                                         .requestEmail()
                                                         .build();

        // [START build_client]
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                                .enableAutoManage(this, this)
                                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                                .build();
    }

    @Override
    public void onStart()
    {
        super.onStart();

        OptionalPendingResult<GoogleSignInResult> opr = Auth.GoogleSignInApi.silentSignIn(mGoogleApiClient);
        if (opr.isDone())
        {
            Log.d(TAG, "Got cached sign-in");
            GoogleSignInResult result = opr.get();
            handleSignInResult(result);
        }
        else
        {
            opr.setResultCallback(new ResultCallback<GoogleSignInResult>()
            {
                @Override
                public void onResult(GoogleSignInResult googleSignInResult)
                {
                    handleSignInResult(googleSignInResult);
                }
            });
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        super.onActivityResult(requestCode, resultCode, data);

        // Result returned from launching the Intent from GoogleSignInApi.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN)
        {
            GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(data);
            handleSignInResult(result);
            if(result.isSuccess())
            {
                Intent intent = new Intent(context, AllStreamActivity.class);
                setNewActivityIntent(intent);
                startActivity(intent);
            }
        }
        else if (requestCode == RC_SIGN_OUT)
        {
            GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(data);
            handleSignInResult(result);
        }
    }

    // [START handleSignInResult]
    private void handleSignInResult(GoogleSignInResult result)
    {
        if (result.isSuccess()) {
            // Signed in successfully, show authenticated UI.
            acct = result.getSignInAccount();
        }
        else
        {
            // Signed out, show unauthenticated UI.
            findViewById(R.id.sign_in_status).setVisibility(View.VISIBLE);
        }
        updateUI();
    }

    // [START signIn]
    private void signIn()
    {
        Intent signInIntent = Auth.GoogleSignInApi.getSignInIntent(mGoogleApiClient);
        startActivityForResult(signInIntent, RC_SIGN_IN);
    }

    // [START signOut]
    private void signOut()
    {
        Auth.GoogleSignInApi.signOut(mGoogleApiClient).setResultCallback(
                new ResultCallback<Status>() {
                    @Override public void onResult(Status status) {updateUI();}
                });
        acct = null;
    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult)
    {
        findViewById(R.id.sign_in_status).setVisibility(View.VISIBLE);
    }

    @Override
    protected void onStop()
    {
        super.onStop();
    }


    private void updateUI()
    {
        if(acct != null)
        {
            findViewById(R.id.button_sign_in).setVisibility(View.GONE);
            findViewById(R.id.button_sign_out).setVisibility(View.VISIBLE);
        }
        else
        {
            findViewById(R.id.button_sign_in).setVisibility(View.VISIBLE);
            findViewById(R.id.button_sign_out).setVisibility(View.GONE);
        }
    }

    private void setNewActivityIntent(Intent intent)
    {
        if(acct == null)
        {
            return;
        }

        intent.putExtra("userName", acct.getDisplayName());
        intent.putExtra("userEmail", acct.getEmail());
        intent.putExtra("userId", acct.getId());
        intent.putExtra("userToken", acct.getIdToken());
    }

    @Override
    public void onClick(View v)
    {
        switch (v.getId())
        {
            case R.id.button_sign_in:
                signIn();
                break;
            case R.id.button_sign_out:
                Toast.makeText(context, "Signing out", Toast.LENGTH_SHORT).show();
                signOut();
                break;
            case R.id.button_view_streams:
                Intent intent = new Intent(context, AllStreamActivity.class);
                setNewActivityIntent(intent);
                startActivity(intent);
                break;
        }
    }
}
