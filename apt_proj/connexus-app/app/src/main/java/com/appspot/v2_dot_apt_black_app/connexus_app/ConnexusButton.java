package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.util.Log;
import android.view.View;
import android.widget.LinearLayout;

import com.google.gson.JsonObject;

/**
 * Created by brice on 10/23/17.
 */

public class ConnexusButton extends android.support.v7.widget.AppCompatButton implements AsyncResponse
{
    String name;
    Context context;
    Drawable backGd;
    DownloadTask asyncTask = new DownloadTask();
    JsonObject json;
    Intent singleViewIntent;

    @Override
    public void processFinish(Drawable output){
        this.backGd = output;

        if(output == null)
        {
            return;
        }

        Bitmap b = ((BitmapDrawable)backGd).getBitmap();

        if(!name.isEmpty())
        {
            // TODO: Draw text on image
        }

        Bitmap bitmapResized = Bitmap.createScaledBitmap(b, 150, 150, false);
        this.setBackgroundDrawable(new BitmapDrawable(getResources(), bitmapResized));
    }

    public ConnexusButton(final Context con, JsonObject jObj, Intent intent)
    {
        super(con);
        this.context = con;
        json = jObj;
        singleViewIntent = intent;

        if(json != null)
        {
            int len = 10;
            name = json.get("stream_name").toString();
            if(name.length() > len)
            {
                name = name.substring(0, len+1);
            }

            asyncTask.delegate = this;
            asyncTask.execute(json.get("cover_image").getAsString().replace("\"", ""));
        }
        else
        {
            this.setText("Empty");
            this.setTextSize(8);
            setClickable(false);
            return;
        }

        /*
            A JsonObject has the following structure:
            {
                "stream_name":"basketball",
                "key_url":"ag9zfmFwdC1ibGFjay1hcHByEwsSBlN0cmVhbRiAgICAvJ-bCgw",
                "subscribers":[],
                "cover_image":"https://i5.walmartimages.com/asr/d0f3658b-3cf8-459d-ad14-f300c2495836_1.4287fec35da69e2633d03c7f46990a56.jpeg?odnHeight=450&odnWidth=450&odnBg=FFFFFF",
                "key_id":"5700305828184064",
                "owner":"vasic@utexas.edu"
            }

                   Store the image on the phone with name the cover url.
         */
        this.setClickable(true);
        this.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1.0f));

        this.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view)
            {
                singleViewIntent.setClass(context, SingleStreamActivity.class);
                singleViewIntent.putExtra("stream_name", name = json.get("stream_name").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("owner", name = json.get("owner").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("key_url", name = json.get("key_url").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("key_id", name = json.get("key_id").getAsString().replace("\"", ""));
                context.startActivity(singleViewIntent);
            }
        });
    }

}
