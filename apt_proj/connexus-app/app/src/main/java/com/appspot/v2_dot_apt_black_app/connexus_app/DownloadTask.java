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
        //private Drawable downloadImage(String url)
        //{
        try {
            Log.i("==> ", url);
            //url = "https://i.pinimg.com/736x/66/b5/2c/66b52cd3106ef7e61856717899b1fa2b--corgi-pups-welsh-corgi-puppies.jpg";
            InputStream is = (InputStream) new URL(url).openStream();
            Drawable d = Drawable.createFromStream(is, "src");
            return d;
        } catch (Exception e) {
            e.printStackTrace();
            Log.i("==> ", "NULL--");
            return null;
        }
    }

    @Override
    protected void onPostExecute(Drawable backGnd) {
        delegate.processFinish(backGnd);
    }
}

