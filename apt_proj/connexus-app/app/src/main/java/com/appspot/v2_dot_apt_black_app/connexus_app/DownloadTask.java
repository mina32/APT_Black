package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.util.Log;

import java.io.InputStream;
import java.net.URL;

/**
 * Created by kking on 10/24/17.
 */

public class DownloadTask extends AsyncTask<String, Integer, Drawable> {
    public AsyncResponse delegate = null;

    @Override
    protected Drawable doInBackground(String... urls) {
        String url = urls[0];

        try
        {
            Log.i("==> ", url);
            InputStream is = (InputStream) new URL(url).openStream();
            Drawable d = Drawable.createFromStream(is, "src");
            return d;
        }
        catch (Exception e)
        {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    protected void onPostExecute(Drawable backGnd) {
        delegate.processFinish(backGnd);
    }
}

