using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SnakePart : MonoBehaviour {
	public static List<SnakePart> SnakeParts = new List<SnakePart>();


	public GameObject Prefab;
	public SnakePart AttachedPart;
	private Rigidbody2D body;

	private int number;
	public int Number
	{
		get{
			return number;
		}
		set {
			number = value;
		}
	}

	public Vector2 Velocity
	{
		get{
			return body.velocity;
		}
		set{
			body.velocity = value;
		}
	}

	public void Start () {
		body = gameObject.GetComponent<Rigidbody2D> ();
		SnakeParts.Add (this);
	}
	
	// Update is called once per frame
	public void Update () {
		if (AttachedPart) {
			body.velocity = (AttachedPart.transform.position - transform.position);
		} else {
			body.velocity = ((Vector2)Camera.main.ScreenToWorldPoint (Input.mousePosition) - (Vector2)transform.position);
		}
	}

	public void OnTriggerEnter2D(Collider2D collider)
	{
		if (!AttachedPart) {
			Instantiate (collider.gameObject).transform.position = new Vector2 (
				Random.Range (-Camera.main.orthographicSize * Camera.main.aspect, Camera.main.orthographicSize * Camera.main.aspect),
				Random.Range (-Camera.main.orthographicSize, Camera.main.orthographicSize));

			Destroy (collider.gameObject);
			createPart ();
		}
	}

	void createPart()
	{
		SnakePart snakePart = Instantiate (Prefab).GetComponent<SnakePart> ();
		snakePart.AttachedPart = SnakeParts [SnakeParts.Count - 1];
		Vector3 offset = -snakePart.AttachedPart.Velocity.normalized * .25f;
		snakePart.transform.position = snakePart.AttachedPart.transform.position + offset;
	}
}
