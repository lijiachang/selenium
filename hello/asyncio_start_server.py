import asyncio

CRLF = b'\r\n'  # 回车换行
PROMPT = b'?>'  # 提示


async def handle_queries(reader, writer):
    """处理查询
    :param reader: asyncio.StreamReader对象
    :param writer: asyncio.StreamWriter对象
    """
    while True:  # 循环处理会话，直到客户端收到控制字符退出。
        writer.write(PROMPT)  # 这里不能使用await，StreamReader.write方法不是协程，只是普通函数
        await writer.drain()  # 协程：drain方法刷新writer缓冲，是协程。
        data = await reader.readline()  # 协程：返回一个bytes对象。

        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = '\x00'  # Telnet发送的控制字符，可能无法decode，此时置位空白字符

        client = writer.get_extra_info('peername')  # 返回与套接字连接的远程地址。
        print('Received from {}:{!r}'.format(client, query))
        if query:
            if ord(query[:1]) < 32:  # 如果收到控制字符或者空字符，退出循环。 ord返回对应字符的ascii码
                break
            send_msg = query + ' ok .'
            if send_msg:
                writer.write(send_msg.encode() + CRLF)  # 转换成bytes对象，并且在每行尾添加回车换行符

            await writer.drain()  # 协程：刷新输出缓冲
            print('Send {} results'.format(len(send_msg)))

    print('Close the client socket')
    writer.close()  # 关闭StreamWriter流


def main():
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, '127.0.0.1', 2323, loop=loop)
    server = loop.run_until_complete(server_coro)

    host = server.sockets[0].getsockname()
    print('Serving on {}'.format(host))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        print('Server shutting down.')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
