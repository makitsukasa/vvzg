using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

// https://dobon.net/vb/dotnet/process/standardoutput.html

public class GetHeadPose : MonoBehaviour {
	private System.Diagnostics.Process p;
	private Vector3 eulerAngles;

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
		p.Kill(); // kore iru ?
		p.Close();
	}

	//OutputDataReceivedイベントハンドラ
	//行が出力されるたびに呼び出される
	void p_OutputDataReceived(object sender,
		System.Diagnostics.DataReceivedEventArgs e)
	{
		try{
			// "(0.0,180.0,180.0)" => Vector3(0.0, 0.0, 0.0)
			var arr = e.Data
				.Replace("(", "")
				.Replace(")", "")
				.Split(',')
				.Select(x => float.Parse(x))
				.ToArray();
			arr[0] -= 9; // related to webcamera angle
			arr[1] = arr[1] + 180;
			arr[2] = (-arr[2] + 270) % 180 + 90; // -90 <= z <= 90
			eulerAngles = new Vector3(arr[0], arr[1], arr[2]);
		}
		catch(System.Exception){

		}
	}

	// Update is called once per frame
	void Update () {
		gameObject.transform.eulerAngles = eulerAngles;
	}
}
