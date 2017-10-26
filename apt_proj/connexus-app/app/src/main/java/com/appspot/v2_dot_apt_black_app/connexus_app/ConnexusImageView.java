package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.widget.LinearLayout;

import com.google.gson.JsonObject;

/**
 * Created by brice on 10/23/17.
 */

public class ConnexusImageView extends android.support.v7.widget.AppCompatImageView implements AsyncResponse
{
    String name;
    Context context;
    Drawable backGd;
    DownloadTask asyncTask = new DownloadTask();
    JsonObject json;
    Intent singleViewIntent;

    @Override
    public void processFinish(Drawable output)
    {
        this.backGd = output;

        if(output == null)
        {
            return;
        }

        Bitmap b = ((BitmapDrawable)backGd).getBitmap();
        Bitmap bitmapResized = Bitmap.createScaledBitmap(b, 250, 250, false);
        this.setBackgroundDrawable(new BitmapDrawable(getResources(), bitmapResized));
    }

    public ConnexusImageView(final Context con, JsonObject jObj, Intent intent)
    {
        super(con);
        this.context = con;
        json = jObj;
        singleViewIntent = intent;

        this.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1.0f));

        if(json != null)
        {
            Log.i("=> ", json.toString());
            asyncTask.delegate = this;
            asyncTask.execute(json.get("image_url").getAsString().replace("\"", ""));
        }
        else
        {
            this.setBackgroundColor(Color.DKGRAY);
        }

        // TODO: Find way to expand a view on click
    }

}
