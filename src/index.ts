import OracleDB from 'oracledb';
import fs, { OpenMode } from 'fs';

async function main(): Promise<number> {
    OracleDB.outFormat = OracleDB.OUT_FORMAT_OBJECT;
    OracleDB.initOracleClient({ libDir: 'C:\\oracle\\instantclient_21_9' });

    const connection = await OracleDB.getConnection({
        user: process.env.ORACLEDB_USER,
        password: process.env.ORACLEDB_PASSWORD,
        connectString: process.env.ORACLEDB_CONNECTIONSTRING,
    }).catch((err) => {
        console.error(err);
    });
    if (!connection) { return -1; }

    // fs.writeFileSync('all_tab_cols.json', JSON.stringify(await connection.execute("select * from all_tab_cols ").catch((err) => {
    //     console.error(err);
    // })));
    
    const OWNER = process.env.ORACLEDB_OWNER;
    const COUNT_STATEMENT = 'COUNT(*)'

    const res = (await connection.execute(`select ${COUNT_STATEMENT} from all_tab_cols where OWNER = '${OWNER}'`).catch((err) => console.log(err)));
    const count = (res as { rows: {'COUNT(*)': number}[] }).rows[0]['COUNT(*)'];
    if (!count) { console.log(res) } else {
        console.log(count);

        let curr_count = 0;

        // open file
        const file = fs.openSync('all_tab_cols.json', 'w');
        fs.writeSync(file, '[');
        
        let i = 0;
        const STEPSIZE = 1000;

        while (STEPSIZE * i < count) {
            const res = await connection.execute(`select * from all_tab_cols where OWNER = '${OWNER}' OFFSET ${STEPSIZE * i} ROWS FETCH NEXT ${STEPSIZE} ROWS ONLY`).catch((err) => {
                console.error(err);
            });
            if (!res) { continue; }

            const rows = (res as { rows: { OWNER: string, TABLE_NAME: string }[] }).rows;
            for (const row of rows) {
                curr_count++;
                fs.writeSync(file, JSON.stringify(row) + (curr_count < count ? ',' : ''));
            }
            i++;
            console.log(`${STEPSIZE * i} of ${count} done`);
        }
        fs.writeSync(file, ']');
    }

    // console.log(
    //     await connection.execute(`select DISTINCT OWNER, TABLE_NAME from all_tab_cols where OWNER = '${OWNER}'`)
    //         .catch((err) => {
    //             console.error(err);
    //         })
    //     );
    return 0;
}

main().catch((err) => {
    console.error(err);
    process.exit(-1);
}).then((code) => {
    if (!code) { code = -1; }
    process.exit(code);
});
