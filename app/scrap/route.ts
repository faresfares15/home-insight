import {NextResponse} from "next/server";
import {exec} from "child_process";

export async function GET(){

        const dataPromise = new Promise((resolve, reject) => {
            exec('source venv/bin/activate && python main.py', (error, stdout, stderr) => {
                if (error) {
                    console.error(`error: ${error.message}`);
                    reject(error);
                }
                resolve(stdout);
        })

    })

    return NextResponse.json({message: "Hello World!"});
}