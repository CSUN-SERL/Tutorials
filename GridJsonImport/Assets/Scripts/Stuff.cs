using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.UI;
using Newtonsoft.Json; //Need this for importing multidimensional array.


public class Stuff : MonoBehaviour {

	// Use this for initialization

	//private string gameDataFileName = "GridJson.json";
    string filePath;
    string jsonString;

    //public Text jsonText;
    public Text test;


    //Floor Tiles
    public Transform FallTile;
    public Transform FloorTile;


    //Class to hold map grid data.
    Map map;

    void Start () {
        //handling file input
        filePath = Application.streamingAssetsPath + "/GridJson.json";
		if (File.Exists (filePath)) {
            //jsonText.text = File.ReadAllText (filePath);
            //string json = System.IO.File.ReadAllText(filePath);
            jsonString = File.ReadAllText(filePath);
            //used to output text to unity display
            test.text = File.ReadAllText(filePath);

        } else {
			Debug.LogError ("Cannot load game data.");
		}

        //Converting json text into object
        //compiler complains: null reference exception
        //map = JsonUtility.FromJson<Map>(jsonString);
        map = JsonConvert.DeserializeObject<Map>(jsonString);

		//Generate Floor
        //The 2D input array has to be nxn
		for (int z = 0; z < map.map.Length; z++) {
            for (int x = 0; x < map.map.Length; x++) {
                //need an if statement in here to handle floor tile logic
                //going to have 1 represent a floor tile and 0 be an empty space


                if (map.map[x][z] == 1)
                {
                    Instantiate(FloorTile, new Vector3(x, 0, z), Quaternion.identity);
                } else
                {
                    Instantiate(FallTile, new Vector3(x, 0, z), Quaternion.identity);
                }


                    /*
                    if (map.map[x][z] == 1) { 
                        GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
                        cube.transform.position = new Vector3(x, 0, z);
                    } else {
                        GameObject cube2 = GameObject.CreatePrimitive(PrimitiveType.Cube);
                        cube2.transform.position = new Vector3(x, 0, z);
                    }*/

                    //This code generates a floor without reading in from json.
                    //GameObject cube = GameObject.CreatePrimitive (PrimitiveType.Cube);
                    //cube.AddComponent<Rigidbody>();
                    //cube.transform.position = new Vector3 (x, 0, z);
                }
		}
	}
}

[System.Serializable] //adds attribute to class: means its serializable
public class Map
{
    public int[][] map;
}