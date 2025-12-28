import crypto from "node:crypto";
import { authenticate } from "./build/release.js";

const target = "ccaf33e3512e31f3";
const start = new Date("2025-12-21T23:00:00+08:00").getTime();
const end   = new Date("2025-12-22T03:00:00+08:00").getTime();

console.log(`Searching from ${new Date(start).toLocaleString()} to ${new Date(end).toLocaleString()}`);

for (let t = start; t <= end; t += 1) {
    globalThis.Date.now = () => t;
    const authResult = authenticate("admin", "admin");
    const authData = JSON.parse(authResult);
    const md5 = crypto.createHash("md5").update(JSON.stringify(authData)).digest("hex");
    if (md5.startsWith(target)) {
        console.log("Hit!");
        console.log("Timestamp:", t);
        console.log("MD5:", md5);
    }
}
