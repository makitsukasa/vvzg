using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// https://dobon.net/vb/dotnet/process/standardoutput.html

public class GetHeadPose : MonoBehaviour {
	private System.Diagnostics.Process p;
	// Use this for initialization
	void Start () {
		//Processオブジェクトを作成
		p = new System.Diagnostics.Process();

		//出力をストリームに書き込むようにする
		p.StartInfo.UseShellExecute = false;
		p.StartInfo.RedirectStandardOutput = true;
		//OutputDataReceivedイベントハンドラを追加
		p.OutputDataReceived += p_OutputDataReceived;

		p.StartInfo.FileName =
			System.Environment.GetEnvironmentVariable("ComSpec");
		p.StartInfo.RedirectStandardInput = false;
		p.StartInfo.CreateNoWindow = true;
		p.StartInfo.Arguments = @"/c python Assets/HeadPoseEstimation/main.py /w";

		//起動
		p.Start();

		//非同期で出力の読み取りを開始
		p.BeginOutputReadLine();
	}

	void OnDestroy(){
		// p.WaitForExit();
		p.Kill(); // ?
		p.Close();
	}

	//OutputDataReceivedイベントハンドラ
	//行が出力されるたびに呼び出される
	static void p_OutputDataReceived(object sender,
	System.Diagnostics.DataReceivedEventArgs e)
	{
		//出力された文字列を表示する
		Debug.Log(e.Data);
	}

	// Update is called once per frame
	void Update () {

	}
}
